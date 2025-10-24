import logging

from pydantic_ai import Agent, RunContext

from opus_agent_base.tools.fastmcp_client_helper import FastMCPClientHelper
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class EnrichedIssue(BaseModel):
    issue_id: str
    issue_title: str
    component: str
    service: str
    is_new_feature: bool = True
    is_enhancement: bool = False

class JiraIssuesHigherOrderTool(HigherOrderTool):
    """
    Jira issues tools on top of Jira MCP that can be added to the agent
    """

    def __init__(self, config_manager=None, instructions_manager=None, model_manager=None):
        super().__init__("jira", "sde.project_management.jira", config_manager, instructions_manager, model_manager)
        self.fastmcp_client_helper = FastMCPClientHelper()
        self.init_agent()

    def init_agent(self):
        model = self.model_manager.get_model()
        self.agent = Agent(
            instructions=self.instructions_manager.get("jira_issue_assistant_instructions"),
            model=model,
            output_type=EnrichedIssue
        )

    async def initialize_tools(self, agent, fastmcp_client_context):
        @agent.tool
        async def jira_issue_classifier(
            ctx: RunContext[str],
            atlassian_cloud_id: str,
            jira_issue_id: str,
        ) -> EnrichedIssue:
            """
            Classify a Jira issue.
            The input requires Atlassian Cloud ID. Use the tool `jira_getAccessibleAtlassianResources` to get the Atlassian Cloud ID.
            The input contains Jira issue id.

            The output is the classification of the issue, according to the requirements specified in the structured output.

            Render the extracted features in the format of `EnrichedIssue`.
            If there are some features which cannot be extracted, set the value to `None`.
            """
            try:
                logging.info(f"""[HigherOrderToolCall] Classifying jira issue {jira_issue_id}:
                Atlassian Cloud ID: {atlassian_cloud_id}
                """)

                # Get issue details using jira_getJiraIssue tool
                issue_details = await self.fastmcp_client_helper.call_fastmcp_tool(
                    fastmcp_client_context,
                    "jira_getJiraIssue",
                    {
                        "issueIdOrKey": jira_issue_id,
                        "cloudId": atlassian_cloud_id
                    },
                    parse_json=True
                )
                # Extract JSON fields
                logging.debug(f"Issue details {jira_issue_id} - {issue_details}")
                logging.debug(f"Issue details {jira_issue_id} - {type(issue_details)}")
                issue_title = issue_details.get("data", {})[0].get("fields", {}).get("summary", "")
                issue_description = issue_details.get("data", {})[0].get("fields", {}).get("description", "")
                logging.info(f"Received Issue summary {jira_issue_id} - {issue_title}")
                # create prompt
                # use agent to extract features of the issue
                prompt_template = self.instructions_manager.get("jira_issue_classifier")
                prompt = prompt_template.format(
                    issue_id=jira_issue_id,
                    issue_title=issue_title,
                    issue_description=issue_description,
                    issue_details=issue_details
                )
                response = await self.agent.run(prompt)
                enriched_issue = response.output
                logging.info(f"""[HigherOrderToolCall] Classified jira issue {jira_issue_id}. Output:
                {enriched_issue}
                """)
                return enriched_issue
            except Exception as e:
                import traceback
                logging.error(f"Stacktrace: {traceback.format_exc()}")
                logging.error(f"Error extracting features of the issue: {e}")
                raise