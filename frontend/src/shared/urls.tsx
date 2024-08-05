export const flaskApiUrl = "https://backend-service-dot-cs467-jhaiwt-431408.wl.r.appspot.com";

const regex = new RegExp("localhost");

export const baseBackendUrl: string = regex.test(window.location.href)
  ? "http://localhost:8080"
  : flaskApiUrl;
