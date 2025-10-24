import logging

from pydantic_ai import Agent, RunContext

from opus_agent_base.tools.fastmcp_client_helper import FastMCPClientHelper
from opus_agent_base.tools.higher_order_tool import HigherOrderTool

logger = logging.getLogger(__name__)


class GithubIssuesHigherOrderTool(HigherOrderTool):
    """
    Github issues tools on top of Github MCP that can be added to the agent
    """

    def __init__(self, config_manager=None, instructions_manager=None, model_manager=None):
        super().__init__("github", "sde.project_management.github", config_manager, instructions_manager, model_manager)
        self.fastmcp_client_helper = FastMCPClientHelper()
        self.init_agent()

    def init_agent(self):
        model = self.model_manager.get_model()
        self.agent = Agent(
            instructions=self.instructions_manager.get("github_issues_assistant_instructions"),
            model=model,
        )


    async def initialize_tools(self, agent, fastmcp_client_context):
        @agent.tool
        async def generate_acceptance_criteria_for_github_issue(
            ctx: RunContext[str],
            github_issue_url: str,
            requirement_description: str,
            requirement_context_type: str,
            requirement_context_source_type: str,
            requirement_context_source_value: str
        ) -> str:
            """
            Generate acceptance criteria for a Github issue.

            The input should contain a brief requirement description. If the user has not provided brief requirement description, ask them for this input.

            The input should contain the context type and source of the requirement.
            The context type can be one of the following:
            - code
            - document

            The context source type for code can be one of the following. Context source value is the actual file path or github url:
            - file
            - github_url

            The context source for document can be one of the following. Context source value is the actual confluence page url:
            - confluence_page

            The output is the acceptance criteria.

            Ask the user for approval of acceptance criteria.
            If the user approves, update the acceptance criteria in Github issue using the tool `github_update_issue`.
            If the user provides feedback, revise the acceptance criteria and ask for approval again.
            """
            try:
                logging.info(f"""[HigherOrderToolCall] Generating Acceptance criteria for Github issue {github_issue_url}:
                 context_type: {requirement_context_type}, context_source_type: {requirement_context_source_type}, context_source_value: {requirement_context_source_value}, requirement_description: {requirement_description}
                 """)
                if requirement_context_type == "code":
                    if requirement_context_source_type == "file":
                        # get issue title
                        # Parse owner, repo, and issue number from github_issue_url
                        # Expected format: https://github.com/owner/repo/issues/123
                        url_parts = github_issue_url.rstrip('/').split('/')
                        issue_number = int(url_parts[-1])
                        repo = url_parts[-3]
                        owner = url_parts[-4]

                        # Get issue details using github_get_issue tool
                        issue_details = await self.fastmcp_client_helper.call_fastmcp_tool(
                            fastmcp_client_context,
                            "github_get_issue",
                            {
                                "owner": owner,
                                "repo": repo,
                                "issue_number": issue_number
                            }
                        )
                        issue_title = issue_details.get("title", "")
                        # get code context from file
                        code_context = self.read_file(requirement_context_source_value)
                        # create prompt
                        # use agent to generate acceptance criteria
                        prompt_template = self.instructions_manager.get("acceptance_criteria_for_github_issue_from_code")
                        prompt = prompt_template.format(
                            issue_title=issue_title,
                            issue_description=requirement_description,
                            code=code_context
                        )
                        response = await self.agent.run(prompt)
                        acceptance_criteria = response.output
                        return acceptance_criteria
                    elif requirement_context_source_type == "github_url":
                        raise ValueError("Github url of the file is not yet supported")
                elif requirement_context_type == "document":
                    if requirement_context_source_type == "confluence_page":
                        raise ValueError("Confluence page url is not yet supported")
                else:
                    raise ValueError("Invalid context type or source")
            except Exception as e:
                import traceback
                logging.error(f"Stacktrace: {traceback.format_exc()}")
                logging.error(f"Error generating acceptance criteria: {e}")
                raise

    def read_file(self, file_path: str) -> str:
        with open(file_path, "r") as f:
            file_content = f.read()
        return file_content
