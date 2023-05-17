import { http } from "@/utils/http";

export const getAnimationsList = () => {
  return http.get("/animations");
};

export const loadAnimation = (animationId) => {
  return http.get(`/animation/${animationId}`);
};

export const createAnimation = (data, params = {}) => {
  return http.post("/animations", data, { params });
};

export const deleteAnimation = (animationId) => {
  return http.delete(`/animation/${animationId}`);
};

export const updateAnimation = (animationId, data) => {
  return http.patch(`/animation/${animationId}`, data);
};
