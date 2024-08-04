export const flaskApiUrl = "https://backend-service-dot-cs467-jhaiwt-431408.wl.r.appspot.com";

export const developmentBackendUrl = "http://localhost:8080/";

const regex = new RegExp("localhost");

export const baseBackendUrl: string = regex.test(window.location.href)
  ? developmentBackendUrl
  : flaskApiUrl;