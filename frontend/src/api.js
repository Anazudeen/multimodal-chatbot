import axios from "axios";

const API = "http://127.0.0.1:8000";

export async function uploadPDF(file) {
  const form = new FormData();
  form.append("file", file);
  return axios.post(`${API}/upload/pdf`, form);
}

export async function uploadImage(file) {
  const form = new FormData();
  form.append("file", file);
  return axios.post(`${API}/upload/image`, form);
}

export async function askLLM(query, imageName = null) {
  return axios.post(`${API}/chat`, { query, image_name: imageName });
}
