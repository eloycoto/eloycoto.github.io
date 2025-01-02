Can an LLM Just Get It?
=========================
:date: 2025-01-02 13:00
:language: en-GB
:author: eloycoto
:tags: AI
:head: Can an LLM Just Get It?
:index_title: Using LLMs for Security Vulnerability Detection
:metatitle: Can LLMs Help Prevent Security Vulnerabilities? A Practical Example
:metatags: security, LLM, AI, vulnerability detection, Spring Boot, actuator, heapdump, cybersecurity, automation
:description: Exploring how Large Language Models (LLMs) can be used to detect security vulnerabilities, inspired by the VW Group data leak incident discussed at 38C3. Includes a practical approach combining traditional security tools with LLMs.
:keywords: LLM, security, vulnerability detection, Spring Boot, actuator, heapdump, subfinder, gobuster, AI security, cybersecurity automation, 38C3, VW Group

Recently I've read a lot of security-related stuff, mainly because of
the awesome `38C3 <https://events.ccc.de/congress/2024/infos/index.html>`_
conference. In that conference, there was a disclosure about how the VW Group
stores multiple insights about their cars. More info can be found `here
<https://x.com/alex_avoigt/status/1873315392082334150>`_ (summary) and `here
<https://media.ccc.de/v/38c3-wir-wissen-wo-dein-auto-steht-volksdaten-von-volkswagen>`__
(talk in German):

They gained access through of an enabled debugging path in a Spring Boot
application, where the heap dump could be found at `actuator/heapdump`. From
there, some credentials for a MongoDB and a few TB of data were stolen.

So, the question is, **can an LLM help prevent this kind of issue?** I played
around a bit and ended up with something like this:

1) `subfinder <https://github.com/projectdiscovery/subfinder>`_ to look at all subdomains related to a domain
2) `gobuster <https://github.com/OJ/gobuster>`_ to track the paths which might cause a problem
3) Get the output from the previous commands, and ask your favorite LLM if there are any security risks

I made a test, and I ended up with an output like this:

.. code-block:: markdown

    **RISK: MEDIUM**
    RESOURCE: https://springtest.acalustra.com/actuator/heapdump
    REASON: The presence of an Actuator endpoint (`heapdump`) on a publicly accessible server suggests a potential vulnerability in the web application's configuration or security settings. This could allow unauthorized access to sensitive information, such as memory dumps.

LLMs are manageable, and you can do quite a lot of things with them. From
structured output to checking if that path is white listed or already triaged.
I ended up doing my test using `PDL
scripts <https://ibm.github.io/prompt-declaration-language/>`__, and it looks as
simple as this:

.. code-block:: yaml


    description: Security checks for web
    text:

    - def: DOMAIN
      text: "mydomain.org"

    - def: SUBDOMAINS
      contribute: []
      lang: command
      parser: json
      code: |
        bash -c "subfinder -d ${DOMAIN} -oJ | jq -s '. + [{\"host\":\"${DOMAIN}\"}]'"

    - def: WORDLIST
      text: "wordlists/seclists/Discovery/Web-Content/quickhits.txt"

    - def: BUSTER
      contribute: []
      for:
        domain: ${SUBDOMAINS}
      repeat:
        text:
        - text: "Checking directories for: ${domain.host}"
        - lang: command
          code: |
            bash -x -c "gobuster dir --no-progress -t 50 -s 200,301,302 -b '' -r --url ${domain.host} --wordlist ${WORDLIST} -o - || true"
      join:
        as: array
      join:
        with: "\n"

    - def: SYSTEM_PROMPT
      contribute: []
      text: |
        You are a security analysis assistant specialized in web application security. Your role is to:

        1. Analyze security scan results from tools like subfinder (subdomain enumeration) and gobuster (directory brute forcing)

        2. Identify potential security risks based on:
           - Exposed sensitive endpoints
           - Development/testing environments
           - Administrative interfaces
           - System files and directories
           - API endpoints and documentation
           - Database management interfaces
           - Backup or version control files

        3. For each finding:
           - Assess the risk level based on potential impact
           - Provide clear reasoning for why it's a security concern
           - Consider the full context of the finding
           - Avoid false positives by considering common legitimate uses

        4. Format findings consistently and clearly, including:
           - Risk level (CRITICAL, MAJOR, MEDIUM, LOW)
           - Full resource URL
           - Clear, specific explanation of the security risk

        5. Use these risk levels appropriately:
           - CRITICAL: Direct security impact (exposed credentials, admin interfaces)
           - MAJOR: Significant security concerns (sensitive data exposure, development environments)
           - MEDIUM: Potential security issues requiring investigation
           - LOW: Minor security concerns or information disclosure

        6. Be thorough but avoid false alarms. Consider legitimate uses and context when assessing risks.

        You should maintain a professional, security-focused tone and provide actionable insights.

    - def: INPUT
      contribute: []
      text:
      - |
        Analyze security scan results for domain `${DOMAIN}`

        Our subfinder scan found these subdomains:
        ```
        ${SUBDOMAINS}
        ```

        Our gobuster directory scan results:
        ```
        ${BUSTER}
        ```

        Please analyze for security risks and provide findings in this format:

        RISK: [CRITICAL|MAJOR|MEDIUM|LOW]
        RESOURCE: <full URL of the potentially vulnerable resource>
        REASON: <clear explanation in 2-3 lines about why this presents a security risk>

        Notes:
        - Consider both subdomain enumeration and directory scanning results
        - Evaluate each finding's context and potential impact
        - Include full URLs (https://) in resources


    - model: openai/llama3.2:3b
      input:
        array:
          - role: system
            content: ${SYSTEM_PROMPT}
          - role: user
            content: ${INPUT}
      parameters:
        temperature: 0


This is a great example of how simple AI agents can make life easier for a lot
of organizations, and the cost is near zero. Certainly, this can add a bit of
noise, false positives, etc..  However as I said, LLMs are manageable, and
output can be improved to make it useful for your organization.

PS: I also really enjoyed these talks from 38C3:

- `Liberating Wi-Fi on the ESP32 <https://media.ccc.de/v/38c3-liberating-wi-fi-on-the-esp32>`__
- `Hacking yourself a satellite - recovering BEESAT-1 <https://media.ccc.de/v/38c3-hacking-yourself-a-satellite-recovering-beesat-1>`__
- `Breaking NATO Radio Encryption <https://media.ccc.de/v/38c3-breaking-nato-radio-encryption>`__


I also made a nix flake for test this:

.. code-block:: nix

    {
      description = "PDL security checks";
      inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
        flake-utils.url = "github:numtide/flake-utils";
        eloy.url = "github:eloycoto/nix-custom-overlay";
      };
      outputs = { self, nixpkgs, flake-utils, eloy }:
        flake-utils.lib.eachDefaultSystem
          (system:
            let
              pkgs = import nixpkgs {
                inherit system;
                overlays = [eloy.overlays.default];
              };
            in
            with pkgs;
            {
              devShells.default = mkShell {
                buildInputs = [
                  pkgs.gnumake
                  pkgs.python3Packages.prompt-declaration-language
                  pkgs.subfinder
                  pkgs.gobuster
                  pkgs.seclists
                ];
                shellHook = ''
                  rm -rf wordlists
                  ln -sf "${pkgs.seclists}/share/wordlists" ./wordlists
                '';
              };
            }
          );
    }
