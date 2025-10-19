import json
import logging

from mcp.client.session import ClientSession

logger = logging.getLogger(__name__)


class FastMCPClientHelper:
    """
    Helper class for FastMCP client
    """

    def __init__(self):
        pass

    async def call_fastmcp_tool(
        self,
        fastmcp_client_context,
        mcp_tool_name: str,
        kwargs: dict,
        parse_json: bool = True,
    ):
        async def execute_with_session(session: ClientSession):
            result = await session.call_tool(mcp_tool_name, kwargs)
            return self.parse_result(result, parse_json)

        return await fastmcp_client_context(execute_with_session)

    def parse_result(self, result, parse_json):
        if hasattr(result, "content"):
            if parse_json:
                if isinstance(result.content, list):
                    json_result = {
                        "data": [
                            json.loads(str(contentItem.text))
                            for contentItem in result.content
                        ]
                    }
                else:
                    json_result = {"data": json.loads(str(result.content))}
                return json_result
            else:
                if isinstance(result.content, list):
                    text_result = {
                        "data": [
                            str(contentItem.text) for contentItem in result.content
                        ]
                    }
                else:
                    text_result = {"data": str(result.content)}
                return text_result
        else:
            return {"data": str(result)}
