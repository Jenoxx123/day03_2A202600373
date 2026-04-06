import axios from "axios";

async function testAgent() {
  try {
    const response = await axios.post("http://localhost:3001/api/chat", {
      message: "Đặt lịch họp với phuonganh@vinai.io vào ngày 2025-04-07 từ 10:00 đến 11:00 UTC. Tiêu đề là Gặp mặt định kỳ.",
      history: []
    });
    console.log("Agent Response:", JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error("Test Error:", error.response?.data || error.message);
  }
}

testAgent();
