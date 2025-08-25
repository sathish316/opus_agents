This is a container for multiple repositories.

The roles and responsibilities of different modules are explained below:
1. Magnum Opus Agents
"Magnum Opus" is a latin word which means "Your Greatest work" or Masterpiece.
It will be a framework for AI to help Users like JARVIS helps IronMan to do Superhuman things.
There will be specialized Agents, Multi-agent workflows, Opinionated workflows using Magnum Opus for vertical specialities like SDE, SRE, MLE, Financial Planner etc. It is built on top of existing open source frameworks like PydanticAI, LangGraph etc.

This framework takes a contrarian point of view in terms of public opinion on AI:
It does not believe that AI will replace all white collar jobs. Neither does it believe that LLM will have limited capabilities for reasoning to assist complex knowledge work. It hopes that better machine learning, deep learning, language models will emerge in future.  It believes that AI will augment every human like JARVIS in Iron man to do things that were not possible before. Technology has always had exponential growth every 10-20 years and we need to embrace AI and integrate it to optimize work and life. The viewpoints are inspired by Neil De Grasse Tyson's views in this podcast - Link.

Magnum Opus is the base framework, which will help users create vertical specific Agents, Multi-agent workflows, Opinionated workflows that can run on your laptop, containerized sandboxes and remote computers. The name is inspired by Deep Research agents like Manus, whose name comes from the latin word "Mens et Manus" meaning "Mind to Hand". Opus will help us to do the greatest work of our lives and achieve exponential growth in Life, Work, Society using AI.

2. Opus SDE Agents
A collection of Agents that are specialized for SDE workflows and tasks. SDE agents can run on your own laptop, an orchestration engine like Temporal, containerized local environments like Dagger, containerized remote environments on Kubernetes. All Agents and workflows are customizable to suit your individual workflows.

Micro-sprint is an opinionated workflow for executing a set of tasks in a software project and augmenting human programmers.

3. Opus SRE Agents
A collection of Agents that are specialized for Oncall and SRE workflows and tasks. SRE agents can run on your own laptop, an orchestration engine like Temporal, containerized local environments like Dagger, containerized remote environments on Kubernetes. All Agents and workflows are customizable to suit your individual Oncall and SRE workflows.

Bisect-ai is an AI version of debugging code changes, deployments, feature flags that caused your system to fail.

Tailgrep-ai is a AI version of debugging an issue from Log aggregation systems to reason about why your system has failed.

Htop-ai is an AI version of using Monitoring tools to reason about why your system has failed.

Flame-ai is an AI version of using Profiling tools to reason about why your system has degraded in performance.

Opus SRE agents can talk to several Alert management systems like PagerDuty, OpsGenie, your own custom Alerting solution. Agents can talk to several Incident management systems like DataDog, ServiceNow, JiraServiceManagement, your own custom Incident management solution. 

Agents can interact with any part of your DevOps Toolchain to help you troubleshoot, identify root-cause, suggest resolution for a Production alert or incident:
1. Plan - Jira, Linear, Google sheets, TODO.md
2. Code - Github, Gitlab, BitBucket
3. Build - Maven, Gradle
4. Test - SonarQube
5. Release - Github Actions, Gitlab Pipelines, Jenkins
6. Deploy - Github Actions, Gitlab Pipelines, Spinnaker, ArgoCD
7. Operate - Kubernetes, Ansible, Chef
8. Monitor - Prometheus, Grafana, ELK, Splunk, DataDog

4. Opus Productivity Agents
A collection of Agents whose aim is to remove the Busywork that robs you of all your cognitive energies and productive time in life and work. 

Agents can interact with a Plethora of Productivity software that acts as Time suckers, not letting you work on things that actually matter. Think of a Pepper Potts like AI Assistant, that briefs you on all the stuff that matters from Collaboration software. 

Opus Productivity Agents work across these tools, helping you focus on the work that matters and distill the rest:
* Email - Gmail, Outlook
* Chat - Google Chat, Slack
* Meetings - Google Meet, Zoom, Teams
* Meeting recorders - Meet recording, Zoom recording, Loom notetaker
* Documents - Google Docs, Confluence
* Calendar - Google Calendar
* Todo list management - Todoist, Microsoft Todo, Trello
* Notetaking tools - Obsidian, Notion, Apple notes, Org mode

5. Opus MLE Agents
A collection of agents to build ML and Deep learning models on Data.

6. Todo AI
This is a legacy repository that helps to solve some of the problems that Opus Productivity Agents solves. The work required is to port this functionality to Opus Productivity Agents.

7. Micro Sprint
This is a legacy repository that helps to solve some of the problems that Opus SDE Agents solves. The work reuqired is to port the early part of these containerized workflows to Opus SDE Agents.