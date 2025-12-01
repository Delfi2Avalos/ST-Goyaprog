function LogoutButton() {
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    window.location.href = "/";
  };

  return (
    <div style={{ textAlign: "right", marginBottom: "1rem" }}>
      <button
        onClick={handleLogout}
        style={{
          backgroundColor: "#e63946",
          color: "white",
          border: "none",
          padding: "8px 14px",
          borderRadius: "8px",
          cursor: "pointer",
          fontWeight: "bold",
          transition: "0.2s ease",
        }}
      >
        Cerrar sesión
      </button>
    </div>
  );
}
export default LogoutButton;
