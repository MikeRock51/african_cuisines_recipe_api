import readlineSync from "readline-sync";
import colors from "colors";
import OpenAI from "openai";
import dotenv from "dotenv";

dotenv.config();

const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
  throw Error("OPENAI key missing");
}

const openai = new OpenAI({ apiKey: apiKey });

async function main() {
  console.log(
    colors.bold.green(
      "Welcome! My name is Yishu. Your AI assistant for all things nutrition. How may I be of help today?"
    )
  );

  const systemMessage =
    "Your name is Yishu. You are a food and nutrition specialist bot. You provide expert assistance on all matters related to food, nutrition and health";
  const chatHistory = [{ role: "system", content: systemMessage }];

  while (true) {
    const userInput = readlineSync.question(colors.yellow("You: "));
    try {
      const messages = chatHistory;

      messages.push({ role: "user", content: userInput });
      // console.log(messages);

      const completion = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: messages,
      });

      const completionText = completion.choices[0].message.content;
      if (userInput.toLowerCase() === "exit") {
        console.log(colors.green("Yishu: ") + completionText);
        return;
      }

      console.log(colors.green("Yishu ") + completionText);
      chatHistory.push({ role: "user", content: userInput });
      chatHistory.push({ role: "assistant", content: completionText });
    } catch (error) {
      console.error(colors.red(error));
    }
  }
}
main();
