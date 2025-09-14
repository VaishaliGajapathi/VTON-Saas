import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import axios from "axios";

function Model({ url }) {
  const { scene } = useGLTF(url);
  return <primitive object={scene} />;
}

function App() {
  const [file, setFile] = useState(null);
  const [modelUrl, setModelUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post("http://localhost:8000/generate-3d", formData);
      setModelUrl(res.data.model_url);
    } catch (err) {
      alert("Error generating 3D model");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>3D Virtual Try-On SaaS</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Generating..." : "Generate 3D Model"}
      </button>

      {modelUrl && (
        <Canvas style={{ height: "500px", marginTop: "20px" }}>
          <ambientLight />
          <pointLight position={[10, 10, 10]} />
          <Model url={modelUrl} />
          <OrbitControls />
        </Canvas>
      )}
    </div>
  );
}

export default App;
