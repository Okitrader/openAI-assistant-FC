import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
import textwrap

load_dotenv()
# other ways to use openai api
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.organization = os.getenv("OPENAI_ORGANIZATION")

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"

### personal_trainer_assistant = client.beta.assistants.create(
#     name="Personal Trainer",
#     instructions="""You are the highly motivating trainer that
#     everyone wants to work with. You are knowledgeable about crossfit,
#     skiing, and swimming.""",
#     model=model
# )
# asst_id = personal_trainer_assistant.id
# print(asst_id)

# # Thread -- This is where the conversation will take place
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "I want to get in shape. What should I do? focus on skiing."
#         }
#     ]
# )
# thread_id = thread.id
# print(thread_id)

##----Hardcode our ids -- created from the above code
asst_id = 'asst_xjg2mBlqojfGAntczpg0N9q3'
thread_id = 'thread_qh394yj4RxRKfgK2r4ndSeDY'

# === create a message ===
message = "What are some exercises I can do to improve my skiing?"
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message
)

## === Run our assistant ===
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=asst_id,
    instructions='Please address the user as Kenny Powers'
)

##=== Run Helper Function ===

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Waits for run to complete and prints the elapsed time.

    :param client
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: The time to sleep between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# ==== Steps --- Logs ==
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)

# Assuming run_steps.data[0] is an object, manually format a string representation
run_step = run_steps.data[0]
run_step_info = f"ID: {run_step.id}, Status: {run_step.status}, Created At: {run_step.created_at}, Completed At: {run_step.completed_at}"

# Use textwrap to wrap the string at 50 characters wide
run_steps_print = textwrap.fill(run_step_info, width=50)

# Print the wrapped text
print(f"Steps Info Only--->\n{run_steps_print}")
print(f"Steps--->\n{run_steps.data[0]}")
