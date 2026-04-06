import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import axios from "axios";
import { GoogleGenAI } from "@google/genai";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3001;
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
// Use gemini-1.5-flash for stable availability
const modelName = "gemini-2.5-flash";

const bookingTool = {
  functionDeclarations: [
    {
      name: "book_meeting",
      description: "Book a meeting on Google Calendar.",
      parameters: {
        type: "OBJECT",
        properties: {
          targetEmail: { type: "STRING", description: "Email address." },
          startTime: {
            type: "STRING",
            description: "ISO 8601 UTC start time.",
          },
          endTime: { type: "STRING", description: "ISO 8601 UTC end time." },
          meetingTitle: { type: "STRING", description: "Meeting title." },
        },
        required: ["targetEmail", "startTime", "endTime"],
      },
    },
  ],
};

const getSystemPrompt = () => {
  const now = new Date();
  const options = { timeZone: "Asia/Ho_Chi_Minh", hour12: false };
  const vnTime = now.toLocaleString("en-US", options);

  return `You're a meeting assistant. Current time (Vietnam): ${vnTime}. ISO UTC: ${now.toISOString()}. 
  Handle 'ngày mai' (tomorrow), 'ngày kia' (day after tomorrow) correctly. 
  Extract email, ISO start/end times, and title. Only book meetings. Other requests? Reply: 'I only handle bookings.' Relay results clearly.`;
};

async function book_meeting_impl(args) {
  console.log("📅 Booking meeting:", args);
  try {
    const response = await axios.post(process.env.BOOKING_API_URL, {
      targetEmail: args.targetEmail,
      startTime: args.startTime,
      endTime: args.endTime,
      meetingTitle: args.meetingTitle || "Scheduled Meeting",
    });

    if (response.data.status === "ok") {
      return { status: "success", message: "Meeting booked successfully!" };
    } else if (response.data.status === "not ok") {
      return {
        status: "busy",
        reason: "The target person is busy at that time.",
      };
    } else {
      return {
        status: "failed",
        reason: response.data.reason || "Unknown error from booking API.",
      };
    }
  } catch (error) {
    const reason = error.response?.data?.reason || error.message;
    console.error("Booking API error:", reason);
    return { status: "error", reason };
  }
}

app.post("/api/chat", async (req, res) => {
  const { message, history } = req.body;
  console.log("💬 Incoming:", message);

  try {
    // Limit history to last 6 messages to save tokens
    const contents = (history || []).slice(-6).map((h) => ({
      role: h.role === "user" ? "user" : "model",
      parts: [{ text: h.content }],
    }));

    contents.push({ role: "user", parts: [{ text: message }] });

    const systemPrompt = getSystemPrompt();
    // First call: get model's intent (may include a function call)
    const result = await ai.models.generateContent({
      model: modelName,
      contents,
      config: {
        tools: [bookingTool],
        systemInstruction: systemPrompt,
      },
    });

    // Check for function call in response
    const candidate = result.candidates?.[0];
    const parts = candidate?.content?.parts || [];
    const funcCallPart = parts.find((p) => p.functionCall);

    if (funcCallPart) {
      const call = funcCallPart.functionCall;
      console.log("🔧 Tool call:", call.name, call.args);

      const toolResult = await book_meeting_impl(call.args);

      // Second call: send tool result back to model for final response
      const finalResult = await ai.models.generateContent({
        model: modelName,
        contents: [
          ...contents,
          { role: "model", parts: [{ functionCall: call }] },
          {
            role: "tool",
            parts: [
              {
                functionResponse: {
                  name: call.name,
                  response: toolResult,
                },
              },
            ],
          },
        ],
        config: {
          tools: [bookingTool],
          systemInstruction: getSystemPrompt(),
        },
      });

      return res.json({ reply: finalResult.text || "Done." });
    }

    // No function call - plain text response
    const reply = result.text || "I couldn't generate a response.";
    return res.json({ reply });
  } catch (error) {
    console.error("❌ Chat Error:", error.message);
    return res.status(500).json({ error: "Agent encountered an error." });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Agent service running on http://localhost:${PORT}`);
});
