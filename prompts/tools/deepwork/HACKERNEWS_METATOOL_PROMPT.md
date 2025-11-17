Guidelines:
If the user asks a question related to HackerNews APIs:
1. Use the API name topstories_json to get the top stories
1.5 If the user refers to hackernews frontpage, fetch only the first 30 stories
2. Use the API name getItem to get the details of the stories like Title, Time etc.
3. Use the tools `call_dynamic_tool_hackernews_api` to call these APIs with:
    a. api_name: The name of the API to call (required)
    b. Any additional parameters required by that specific API (pass them directly, not wrapped in a dict)
4. Example:
```
call_dynamic_tool_hackernews_api(api_name="topstories_json")
call_dynamic_tool_hackernews_api(api_name="getItem", id="45947810")
```
5. Before returning the result, summarize the stories in this format, with a separator between each story:
* ID
* URL
* Title
* Time
------