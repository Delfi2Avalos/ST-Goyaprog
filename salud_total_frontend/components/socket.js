// WebSocket nativo para Django Channels
let socket = null;

export const conectarSocket = () => {
  const token = localStorage.getItem("token");
  if (!token) {
    console.warn("Intento de conectar WebSocket sin token");
    return;
  }

  const WS_URL = import.meta.env.VITE_API_URL.replace("http", "ws");

  socket = new WebSocket(`${WS_URL}/ws/chat/?token=${token}`);

  socket.onopen = () => {
    console.log("WebSocket conectado a Django Channels");
  };

  socket.onclose = (e) => {
    console.log("WebSocket cerrado:", e.reason);
  };

  socket.onerror = (e) => {
    console.error("Error WebSocket:", e);
  };
};

// Para enviar mensajes
export const enviarMensajeSocket = (data) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(data));
  }
};

// Para recibir mensajes
export const escucharMensajes = (callback) => {
  if (!socket) return;
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    callback(data);
  };
};

export default socket;
