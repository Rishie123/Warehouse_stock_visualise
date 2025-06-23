<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>3D Warehouse Visualizer</title>
  <style>
    body { margin: 0; overflow: hidden; }
    canvas { display: block; }
  </style>
</head>
<body>
  <script src="https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.150.1/examples/js/controls/OrbitControls.js"></script>
  <script>
    const scene = new THREE.Scene();
    scene.background = new THREE.Color('#f0f0f0');

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    camera.position.set(100, 200, 300);

    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(1, 2, 3);
    scene.add(light);

    // Draw godown floors
    const godowns = [
      { name: "Old Godown 1", x: 0, y: 0 },
      { name: "Old Godown 2", x: 60, y: 0 },
      { name: "Old Godown 3", x: 120, y: 0 },
      { name: "New Godown 1", x: 0, y: 120 },
      { name: "New Godown 2", x: 60, y: 120 },
      { name: "New Godown 3", x: 120, y: 120 }
    ];

    godowns.forEach(g => {
      const geometry = new THREE.BoxGeometry(50, 1, 100);
      const material = new THREE.MeshStandardMaterial({ color: '#cccccc' });
      const floor = new THREE.Mesh(geometry, material);
      floor.position.set(g.x + 25, 0.5, g.y + 50);
      scene.add(floor);
    });

    // Example PP bag stack
    const bagGeometry = new THREE.BoxGeometry(3, 10, 3);
    const bagMaterial = new THREE.MeshStandardMaterial({ color: '#9C27B0' });
    const stack = new THREE.Mesh(bagGeometry, bagMaterial);
    stack.position.set(25, 5, 25); // inside Old Godown 1
    scene.add(stack);

    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }

    animate();
  </script>
</body>
</html>
