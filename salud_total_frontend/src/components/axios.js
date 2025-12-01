import axios from "axios";
import { jwtDecode } from "jwt-decode";

const API_URL = import.meta.env.VITE_API_URL;
const FRONT_URL = import.meta.env.VITE_FRONTEND_URL;

// Django: toda la API vive bajo /api/
const api = axios.create({
  baseURL: `${API_URL}/api`,
});

// Rutas públicas del backend Django
const PUBLIC_PATHS = [
  "/auth/login/",
  "/auth/registro/",
  "/auth/refresh/",
];

// Interceptor REQUEST: agrega el token si no es endpoint público
api.interceptors.request.use(
  (config) => {
    const url = config.url || "";
    const isPublic = PUBLIC_PATHS.some((p) => url.startsWith(p));

    if (isPublic) return config;

    const token = localStorage.getItem("access");  // <─ TOKEN DE DJANGO

    if (token) {
      try {
        const { exp } = jwtDecode(token);

        if (Date.now() >= exp * 1000) {
          localStorage.clear();
          if (!isPublic) window.location.href = FRONT_URL;
          return Promise.reject("Token expirado");
        }

        config.headers.Authorization = `Bearer ${token}`;
      } catch (e) {
        console.error("Error decodificando token:", e);
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor RESPONSE
api.interceptors.response.use(
  (r) => r,
  (err) => {
    const url = err?.config?.url || "";
    const isPublic = PUBLIC_PATHS.some((p) => url.startsWith(p));

    // Si Django devuelve 401, deslogueamos
    if (err?.response?.status === 401 && !isPublic) {
      localStorage.clear();
      window.location.href = FRONT_URL;
    }
    return Promise.reject(err);
  }
);

export default api;
