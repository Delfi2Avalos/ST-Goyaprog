const handleLogin = async (e) => {
  e.preventDefault();
  setError("");
  setCargando(true);

  try {
    // Django usa email + password
    const res = await api.post(`/auth/login/`, {
      email,
      password,   // tu backend Django debe aceptar "password"
    });

    const { access, refresh, usuario } = res.data || {};

    if (!usuario || !usuario.tipo) {
      throw new Error("Usuario no válido o sin tipo asignado.");
    }

    // Guardar tokens y datos
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    localStorage.setItem("usuario", JSON.stringify(usuario));

    // Conectar WebSocket
    conectarSocket();

    console.log("Usuario:", usuario.email);
    console.log("Tipo:", usuario.tipo);

    // Ruta según rol
    const rutas = {
      paciente: "/paciente-dashboard",
      medico: "/medico-dashboard",
      admin: "/admin-dashboard",
      superadmin: "/superadmin-dashboard",
    };

    navigate(rutas[usuario.tipo] || "/");

  } catch (err) {
    console.error("Error en login:", err);
    const mensaje =
      err?.response?.data?.mensaje ||
      err?.message ||
      " Error desconocido en inicio de sesión.";
    setError(mensaje);
  } finally {
    setCargando(false);
  }
};
