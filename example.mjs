// example.mjs
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const createCompletion = async () => {
  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo", // Use a valid model name
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        {
          role: "user",
          content: "Write a haiku about recursion in programming.",
        },
      ],
    });

    console.log(completion.choices[0].message);
  } catch (error) {
    console.error("Error creating completion:", error);
  }
};

createCompletion();
