import logging
from typing import List

from pydantic_ai import RunContext

from opus_todo_agent.custom_tools.todo.todoist_client import TodoistClient
from opus_agent_base.helpers.datetime_helper import DatetimeHelper
from opus_todo_agent.helper.todo.todoist_helper import TodoistHelper
from opus_todo_agent.models.todo.todoist_models import CompletedTask, Task

logger = logging.getLogger(__name__)


class TodoistTools:
    """
    Todoist tools that can be added to the agent
    """

    def __init__(self):
        self.todoist_client = TodoistClient()
        self.datetime_helper = DatetimeHelper()
        self.todoist_helper = TodoistHelper()

    def initialize_tools(self, agent):
        @agent.tool
        def get_completed_tasks_for_date_range(
            ctx: RunContext[str], from_date: str, to_date: str
        ) -> List[CompletedTask]:
            """
            Get completed tasks using Todoist Task/Project management from date range from_date to to_date

            Args:
                from_date: Start date in YYYY-MM-DD format
                to_date: End date in YYYY-MM-DD format

            Returns:
                List of CompletedTask objects
            """
            logger.info(
                f"[Tool call] Fetching completed tasks for date range: {from_date} to {to_date}"
            )
            return self.todoist_client.get_completed_tasks_for_date_range(
                from_date, to_date
            )

        @agent.tool
        def get_completed_tasks_for_predefined_date_range(
            ctx: RunContext[str],
            predefined_daterange_key: str,
        ) -> List[CompletedTask]:
            """
            Get completed tasks using Todoist Task/Project management for a predefined date range
            Values of predefined date ranges are:
            1. last_week
            2. today
            3. yesterday
            4. current_week
            """
            logger.info(
                f"[CustomToolCall] Fetching completed tasks for predefined date range: {predefined_daterange_key}"
            )
            if predefined_daterange_key == "last_week":
                since, until = self.datetime_helper.get_last_week_daterange()
            elif predefined_daterange_key == "current_week":
                since, until = self.datetime_helper.get_current_week_daterange()
            elif predefined_daterange_key == "today":
                since, until = self.datetime_helper.get_today_daterange()
            elif predefined_daterange_key == "yesterday":
                since, until = self.datetime_helper.get_yesterday_daterange()
            else:
                raise ValueError(
                    f"Invalid predefined date range key: {predefined_daterange_key}"
                )
            return self.todoist_client.get_completed_tasks_for_date_range(since, until)

        @agent.tool
        def generate_daily_review_of_completed_tasks(
            ctx: RunContext[str],
            predefined_daterange_key: str = None,
            summarize: bool = True,
        ) -> List[CompletedTask]:
            """
            Generate daily review of completed tasks.
            Supported filters for predefined_daterange_key are:
            1. today
            2. yesterday
            3. Specific date in yyyy-mm-dd format

            This method returns a list of completed tasks with project names.

            Generate daily review summary by grouping tasks by project name.

            If the user asks to summarize, return a summary of the completed tasks grouped by project name.
            If a project has more than 5 tasks, try to summarize them within a project.

            If the user asks to not summarize, return the list of completed tasks grouped by project names.

            By default, summarize tasks grouped by project name.
            """
            try:
                if (
                    predefined_daterange_key == ""
                    or predefined_daterange_key == "today"
                ):
                    logging.info("[CustomToolCall] Generating Daily review for today")
                    tasks = get_completed_tasks_for_predefined_date_range(
                        ctx, predefined_daterange_key
                    )
                elif predefined_daterange_key == "yesterday":
                    logging.info("[CustomToolCall] Generating Daily review for yesterday")
                    tasks = get_completed_tasks_for_predefined_date_range(
                        ctx, predefined_daterange_key
                    )
                else:
                    logging.info(
                        f"[CustomToolCall] Generating Daily review for date: {predefined_daterange_key}"
                    )
                    tasks = get_completed_tasks_for_date_range(
                        ctx,
                        predefined_daterange_key,
                        self.datetime_helper.get_next_date(predefined_daterange_key),
                    )
            except Exception as e:
                logging.error(f"Error fetching completed tasks: {e}")
                return

            try:
                project_ids = self.todoist_helper.get_unique_project_ids(tasks)
                project_names = self.todoist_client.get_project_names_for_ids(
                    project_ids
                )
            except Exception as e:
                logging.error(f"Error fetching project names: {e}")
                return

            tasks = [
                task.with_project_name(project_names[task.project_id]) for task in tasks
            ]
            return tasks

        @agent.tool
        def generate_weekly_review_of_completed_tasks(
            ctx: RunContext[str],
            predefined_weekrange_key: str = "current_week",
            from_date: str = "",
            to_date: str = "",
            summarize: bool = True,
        ) -> List[CompletedTask]:
            """
            Generate weekly review of completed tasks.
            Supported filters for predefined_weekrange_key are:
            1. last_week
            2. current_week
            3. Default is current_week if no option is specified

            Instead of predefined_weekrange_key, the user can also provide a from_date and to_date to specify the week range explicitly.

            This method returns a list of completed tasks with project names.

            Generate weekly review summary by grouping tasks by project name.

            If the user asks to summarize, return a summary of the completed tasks grouped by project name.
            If a project has more than 5 tasks, try to summarize them within a project.

            If the user asks to not summarize, return the list of completed tasks grouped by project names.

            By default, summarize tasks grouped by project name.
            """
            try:
                if from_date and to_date:
                    logging.info(
                        f"[CustomToolCall] Generating weekly review for the date range: {from_date} to {to_date}"
                    )
                    tasks = get_completed_tasks_for_date_range(ctx, from_date, to_date)
                elif predefined_weekrange_key == "current_week":
                    logging.info("[CustomToolCall] Generating weekly review for current week")
                    tasks = get_completed_tasks_for_predefined_date_range(
                        ctx, "current_week"
                    )
                elif predefined_weekrange_key == "last_week":
                    logging.info("[CustomToolCall] Generating weekly review for last week")
                    tasks = get_completed_tasks_for_predefined_date_range(
                        ctx, "last_week"
                    )
                else:
                    raise ValueError(
                        f"Invalid date range for weekly review: {predefined_weekrange_key}"
                    )
            except Exception as e:
                logging.error(f"Error fetching completed tasks: {e}")
                return

            try:
                project_ids = self.todoist_helper.get_unique_project_ids(tasks)
                project_names = self.todoist_client.get_project_names_for_ids(
                    project_ids
                )
            except Exception as e:
                logging.error(f"Error fetching project names: {e}")
                return

            tasks = [
                task.with_project_name(project_names[task.project_id]) for task in tasks
            ]
            return tasks

        @agent.tool
        def recommend_tasks_to_focus_on_using_triflow(
            ctx: RunContext[str],
            project_identifier: str = "",
            tag_filter_identifier: str = "",
            count: int = 3,
        ) -> List[Task]:
            """
            Triflow is a method to help you select 3 tasks from a project or a tag to focus on.

            This method helps you to select 3 random tasks from a project. The value of 3 can be changed by the user asking for a different number of tasks.

            This method can also help you to select 3 random tasks from a tag. The value of 3 can be changed by the user asking for a different number of tasks.

            Once you have selected the tasks, you can ask the user to focus on them.
            Display recommended tasks with their project name, task name and a clickable link in parenthesis for each task with the text 'Link'.
            """
            tasks = []
            source_description = ""

            try:
                if project_identifier:
                    logging.info(f"[CustomToolCall] Looking for project: {project_identifier}")

                    # Find the project by name or ID
                    project_id, project_name = (
                        self.todoist_client.find_project_by_name_or_id(
                            project_identifier
                        )
                    )
                    logging.info(f"[CustomToolCall] Found project: {project_name} (ID: {project_id})")

                    # Get all active tasks from the project
                    tasks = self.todoist_client.get_tasks_for_project(project_id)
                    source_description = f"project '{project_name}'"

                elif tag_filter_identifier:
                    logging.info(f"[CustomToolCall] Looking for filter: {tag_filter_identifier}")

                    # Get tasks from filter
                    tasks = self.todoist_client.get_tasks_for_tag(tag_filter_identifier)
                    source_description = f"tagFilter '{tag_filter_identifier}'"

            except Exception as e:
                logging.error(f"Error fetching tasks: {e}")
                return

            if len(tasks) == 0:
                print(f"No active tasks found in {source_description}")
                return

            logging.info(f"Found {len(tasks)} active tasks in {source_description}")

            # Pick random tasks
            selected_tasks = self.todoist_helper.pick_random_tasks(tasks, count)

            try:
                # Fetch project names for all involved project IDs
                project_ids = self.todoist_helper.get_unique_project_ids_from_tasks(
                    selected_tasks
                )
                project_names = self.todoist_client.get_project_names_for_ids(
                    project_ids
                )
            except Exception as e:
                logging.error(f"Error fetching project names: {e}")
                return

            selected_tasks = [
                task.with_project_name(project_names.get(task.project_id, "Unknown"))
                for task in selected_tasks
            ]
            return selected_tasks
