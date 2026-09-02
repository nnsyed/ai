The LangChain Pipeline
-------------------------
Every LangChain application follows the same basic idea.
Input
  ↓
Prompt
  ↓
Model
  ↓
Output


What You Learned
----------------------------------
By the end of this lesson, you've learned the core building blocks:

-------------------------------------------------------------------
Concept						Purpose
-------------------------------------------------------------------
ChatOpenAI			Connects your application to an OpenAI chat model.
.env				Keeps API keys out of your source code.
load_dotenv()		Loads environment variables from the .env file.
invoke()			Sends input to the model and receives a response.
AIMessage			The structured object returned by the model.
response.content	The generated text from the model.
Chat loop			Allows repeated interactions with the model.
-------------------------------------------------------------------

