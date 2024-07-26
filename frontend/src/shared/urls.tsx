export const flaskApiUrl = "";

const regex = new RegExp("localhost");

export const baseBackendUrl: string = regex.test(window.location.href)
  ? "http://localhost:8080"
  : flaskApiUrl;