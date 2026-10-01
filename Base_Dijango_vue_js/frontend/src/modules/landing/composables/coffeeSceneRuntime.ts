import {
  AmbientLight,
  BufferAttribute,
  BufferGeometry,
  CanvasTexture,
  CylinderGeometry,
  DirectionalLight,
  Group,
  HemisphereLight,
  LatheGeometry,
  Mesh,
  MeshStandardMaterial,
  PerspectiveCamera,
  Points,
  PointsMaterial,
  PointLight,
  Scene,
  SphereGeometry,
  SRGBColorSpace,
  TorusGeometry,
  Vector2,
  WebGLRenderer,
} from "three";

export interface CoffeeSceneController {
  setScrollProgress: (progress: number) => void;
  destroy: () => void;
}

/**
 * Creates a dynamic high-resolution texture for the coffee surface
 * featuring rich golden crema and a delicate white latte-art rosette/heart.
 */
function createLatteArtTexture(): CanvasTexture {
  const size = 512;
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");

  if (!ctx) {
    return new CanvasTexture(canvas);
  }

  const cx = size / 2;
  const cy = size / 2;

  // 1. Rich Crema base gradient (deep roasted espresso to golden hazelnut crema)
  const cremaGrad = ctx.createRadialGradient(cx, cy, 30, cx, cy, size / 2);
  cremaGrad.addColorStop(0, "#c9884a"); // center crema
  cremaGrad.addColorStop(0.35, "#a25f2d");
  cremaGrad.addColorStop(0.7, "#6b371b");
  cremaGrad.addColorStop(0.92, "#4a2311");
  cremaGrad.addColorStop(1, "#2e1408"); // dark rim
  ctx.fillStyle = cremaGrad;
  ctx.beginPath();
  ctx.arc(cx, cy, size / 2, 0, Math.PI * 2);
  ctx.fill();

  // 2. Micro-foam texture rings
  ctx.save();
  ctx.globalAlpha = 0.12;
  for (let r = 70; r < size / 2 - 20; r += 28) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.strokeStyle = "#eed5b7";
    ctx.lineWidth = 14;
    ctx.stroke();
  }
  ctx.restore();

  // 3. Latte Art Heart / Rosette in silky cream white
  ctx.save();
  ctx.translate(cx, cy);

  // Outer delicate contrast glow
  ctx.shadowColor = "rgba(70, 32, 12, 0.45)";
  ctx.shadowBlur = 12;

  // Draw Heart / Tulip layers
  const drawTulipPetal = (offsetY: number, scaleX: number, scaleY: number, alpha: number) => {
    ctx.save();
    ctx.translate(0, offsetY);
    ctx.scale(scaleX, scaleY);
    ctx.fillStyle = `rgba(253, 248, 238, ${String(alpha)})`;
    ctx.beginPath();
    ctx.moveTo(0, 10);
    ctx.bezierCurveTo(45, -30, 80, 20, 0, 75);
    ctx.bezierCurveTo(-80, 20, -45, -30, 0, 10);
    ctx.fill();
    ctx.restore();
  };

  // Stacked tulip leaves
  drawTulipPetal(35, 1.15, 0.75, 0.96);
  drawTulipPetal(10, 0.95, 0.65, 0.98);
  drawTulipPetal(-15, 0.75, 0.55, 0.98);
  drawTulipPetal(-38, 0.55, 0.45, 0.98);

  // Center piercing heart top
  ctx.fillStyle = "#fffcf7";
  ctx.beginPath();
  ctx.arc(-16, -62, 14, 0, Math.PI * 2);
  ctx.arc(16, -62, 14, 0, Math.PI * 2);
  ctx.fill();

  // Draw central pull-through line
  const stemGrad = ctx.createLinearGradient(0, -75, 0, 85);
  stemGrad.addColorStop(0, "#ffffff");
  stemGrad.addColorStop(0.6, "#f6ebd8");
  stemGrad.addColorStop(1, "#9e5b29");
  ctx.strokeStyle = stemGrad;
  ctx.lineWidth = 3.5;
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(0, -78);
  ctx.lineTo(0, 85);
  ctx.stroke();

  ctx.restore();

  const texture = new CanvasTexture(canvas);
  texture.colorSpace = SRGBColorSpace;
  return texture;
}

export function createCoffeeScene(canvas: HTMLCanvasElement): CoffeeSceneController {
  const renderer = new WebGLRenderer({
    canvas,
    alpha: true,
    antialias: true,
    powerPreference: "high-performance",
  });
  renderer.setPixelRatio(Math.min(globalThis.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = SRGBColorSpace;

  const scene = new Scene();
  const camera = new PerspectiveCamera(36, 1, 0.1, 100);
  camera.position.set(0, 2.2, 6.2);

  const mainGroup = new Group();
  scene.add(mainGroup);

  // ==========================================
  // Materials
  // ==========================================
  // Fine glossy porcelain / ceramic
  const ceramicMaterial = new MeshStandardMaterial({
    color: 0xfcf9f2,
    roughness: 0.18,
    metalness: 0.04,
  });

  // Warm golden bronze accent trim for cup and saucer
  const goldMaterial = new MeshStandardMaterial({
    color: 0xc58940,
    roughness: 0.3,
    metalness: 0.75,
  });

  // Coffee liquid surface
  const latteArtTexture = createLatteArtTexture();
  const coffeeMaterial = new MeshStandardMaterial({
    map: latteArtTexture,
    roughness: 0.28,
    metalness: 0.05,
  });

  // Roasted coffee bean material
  const beanMaterial = new MeshStandardMaterial({
    color: 0x301a10,
    roughness: 0.42,
    metalness: 0.08,
  });

  // ==========================================
  // 1. Ceramic Cup (True hollow curved Lathe)
  // ==========================================
  const cupPoints: Vector2[] = [
    new Vector2(0.001, 0.0), // center bottom
    new Vector2(0.85, 0.0), // base foot
    new Vector2(0.88, 0.08), // foot bevel
    new Vector2(0.92, 0.22), // lower curve
    new Vector2(1.08, 0.65), // mid body
    new Vector2(1.32, 1.35), // upper flare
    new Vector2(1.42, 1.78), // outer rim
    new Vector2(1.4, 1.84), // rim peak outer
    new Vector2(1.34, 1.84), // rim peak inner
    new Vector2(1.3, 1.75), // inner rim
    new Vector2(1.18, 1.25), // inner wall upper
    new Vector2(0.98, 0.65), // inner wall mid
    new Vector2(0.76, 0.24), // inner bottom edge
    new Vector2(0.001, 0.24), // inner bottom center
  ];
  const cupGeometry = new LatheGeometry(cupPoints, 56);
  const cupMesh = new Mesh(cupGeometry, ceramicMaterial);

  // Cup Gold Rim Trim
  const cupGoldPoints: Vector2[] = [
    new Vector2(1.39, 1.76),
    new Vector2(1.425, 1.84),
    new Vector2(1.345, 1.84),
    new Vector2(1.32, 1.76),
  ];
  const cupGoldGeometry = new LatheGeometry(cupGoldPoints, 56);
  const cupGoldRim = new Mesh(cupGoldGeometry, goldMaterial);

  // ==========================================
  // 2. Liquid Surface with Latte Art
  // ==========================================
  const liquidGeometry = new CylinderGeometry(1.28, 1.24, 0.05, 56);
  const liquidMesh = new Mesh(liquidGeometry, coffeeMaterial);
  liquidMesh.position.y = 1.58;

  // ==========================================
  // 3. Ergonomic Cup Handle
  // ==========================================
  const handleGeometry = new TorusGeometry(0.58, 0.14, 20, 56, Math.PI * 1.55);
  const handle = new Mesh(handleGeometry, ceramicMaterial);
  handle.position.set(1.35, 0.95, 0);
  handle.rotation.set(0, Math.PI / 2, -Math.PI * 0.42);

  // Assemble the Cup Group
  const cupGroup = new Group();
  cupGroup.add(cupMesh, cupGoldRim, liquidMesh, handle);

  // ==========================================
  // 4. Ceramic Saucer (Đĩa lót)
  // ==========================================
  const saucerPoints: Vector2[] = [
    new Vector2(0.001, 0.0), // center underside
    new Vector2(1.15, 0.0), // base rim under
    new Vector2(1.22, 0.06), // foot step
    new Vector2(1.75, 0.15), // gentle body flare
    new Vector2(2.45, 0.42), // raised rim edge
    new Vector2(2.48, 0.48), // outer peak
    new Vector2(2.44, 0.48), // inner peak
    new Vector2(1.7, 0.22), // upper inner slope
    new Vector2(1.05, 0.1), // inner cup indentation ridge
    new Vector2(0.92, 0.06), // cup seat
    new Vector2(0.001, 0.06), // center top
  ];
  const saucerGeometry = new LatheGeometry(saucerPoints, 64);
  const saucer = new Mesh(saucerGeometry, ceramicMaterial);
  saucer.position.y = -0.06;

  // Saucer Gold Edge Ring
  const saucerGoldPoints: Vector2[] = [
    new Vector2(2.44, 0.41),
    new Vector2(2.485, 0.48),
    new Vector2(2.44, 0.48),
    new Vector2(2.4, 0.41),
  ];
  const saucerGoldGeometry = new LatheGeometry(saucerGoldPoints, 64);
  const saucerGoldRing = new Mesh(saucerGoldGeometry, goldMaterial);
  saucerGoldRing.position.y = -0.06;

  // ==========================================
  // 5. 3D Roasted Coffee Beans on Saucer
  // ==========================================
  function createCoffeeBean(): Group {
    const beanGroup = new Group();
    const beanGeom = new SphereGeometry(0.12, 16, 16);
    beanGeom.scale(1, 0.65, 1.45);
    const body = new Mesh(beanGeom, beanMaterial);

    // Dark seam line
    const seamGeom = new CylinderGeometry(0.015, 0.015, 0.32, 8);
    const seamMat = new MeshStandardMaterial({ color: 0x180b06, roughness: 0.9 });
    const seam = new Mesh(seamGeom, seamMat);
    seam.rotation.x = Math.PI / 2;
    seam.position.y = 0.07;

    beanGroup.add(body, seam);
    return beanGroup;
  }

  const bean1 = createCoffeeBean();
  bean1.position.set(1.48, 0.12, 0.85);
  bean1.rotation.set(0.1, 0.6, -0.15);

  const bean2 = createCoffeeBean();
  bean2.position.set(1.72, 0.14, 0.45);
  bean2.rotation.set(-0.15, -0.8, 0.2);

  const bean3 = createCoffeeBean();
  bean3.position.set(-1.42, 0.13, 0.95);
  bean3.rotation.set(0.2, 1.2, 0.1);

  // ==========================================
  // 6. Dynamic Rising Steam Particle Wisps
  // ==========================================
  const steamCount = 38;
  const steamPositions = new Float32Array(steamCount * 3);
  const steamSpeeds: number[] = [];
  const steamDrifts: number[] = [];

  for (let i = 0; i < steamCount; i++) {
    const angle = Math.random() * Math.PI * 2;
    const radius = Math.random() * 0.75;
    steamPositions[i * 3] = Math.cos(angle) * radius;
    steamPositions[i * 3 + 1] = 1.7 + Math.random() * 1.6;
    steamPositions[i * 3 + 2] = Math.sin(angle) * radius;

    steamSpeeds.push(0.008 + Math.random() * 0.012);
    steamDrifts.push(Math.random() * Math.PI * 2);
  }

  const steamGeometry = new BufferGeometry();
  steamGeometry.setAttribute("position", new BufferAttribute(steamPositions, 3));

  const steamMaterial = new PointsMaterial({
    color: 0xf5ede1,
    size: 0.12,
    transparent: true,
    opacity: 0.38,
    depthWrite: false,
  });
  const steamParticles = new Points(steamGeometry, steamMaterial);

  // Add everything to main ensemble
  mainGroup.add(cupGroup, saucer, saucerGoldRing, bean1, bean2, bean3, steamParticles);
  mainGroup.position.set(0, -0.65, 0);

  // ==========================================
  // 7. Studio 3-Point Lighting Setup
  // ==========================================
  // Warm Primary Key Light (upper front-right)
  const keyLight = new DirectionalLight(0xfff3e0, 3.8);
  keyLight.position.set(4.5, 6.0, 4.8);
  scene.add(keyLight);

  // Soft Cool/Cyan Rim Backlight (behind left, highlights glossy porcelain curves)
  const rimLight = new DirectionalLight(0xdcefff, 2.2);
  rimLight.position.set(-4.5, 3.5, -4.0);
  scene.add(rimLight);

  // Warm Golden Accent Light directly on coffee surface
  const topAccentLight = new PointLight(0xffd59e, 2.6, 6.5);
  topAccentLight.position.set(0, 3.4, 0.8);
  scene.add(topAccentLight);

  // Ambient Environment fill
  const hemiLight = new HemisphereLight(0xfff8ee, 0x54321d, 1.8);
  scene.add(hemiLight);

  const ambient = new AmbientLight(0xffffff, 0.7);
  scene.add(ambient);

  // ==========================================
  // 8. Interactive Mouse / Touch Orbit Dragging
  // ==========================================
  let isDragging = false;
  let previousMousePosition = { x: 0, y: 0 };
  let dragRotationX = 0;
  let dragRotationY = 0;
  let dragVelocityX = 0;
  let dragVelocityY = 0;

  const getPointerCoord = (e: MouseEvent | TouchEvent): { x: number; y: number } => {
    if ("touches" in e && e.touches.length > 0 && e.touches[0]) {
      return { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }
    return { x: (e as MouseEvent).clientX, y: (e as MouseEvent).clientY };
  };

  const onPointerDown = (e: MouseEvent | TouchEvent) => {
    isDragging = true;
    previousMousePosition = getPointerCoord(e);
  };

  const onPointerMove = (e: MouseEvent | TouchEvent) => {
    if (!isDragging) return;
    const current = getPointerCoord(e);
    const deltaX = current.x - previousMousePosition.x;
    const deltaY = current.y - previousMousePosition.y;

    dragVelocityY = deltaX * 0.007;
    dragVelocityX = deltaY * 0.005;

    dragRotationY += dragVelocityY;
    dragRotationX += dragVelocityX;

    // Limit pitch angle so it doesn't flip completely upside down
    dragRotationX = Math.max(-0.6, Math.min(0.8, dragRotationX));

    previousMousePosition = current;
  };

  const onPointerUp = () => {
    isDragging = false;
  };

  canvas.addEventListener("mousedown", onPointerDown);
  window.addEventListener("mousemove", onPointerMove);
  window.addEventListener("mouseup", onPointerUp);

  canvas.addEventListener("touchstart", onPointerDown, { passive: true });
  window.addEventListener("touchmove", onPointerMove, { passive: true });
  window.addEventListener("touchend", onPointerUp);

  // ==========================================
  // 9. Render & Animation Loop
  // ==========================================
  let frame = 0;
  let visible = !globalThis.document.hidden;
  let active = true;
  let scrollProgress = 0;
  let targetScrollProgress = 0;

  const render = () => {
    if (!visible || !active) return;
    scrollProgress += (targetScrollProgress - scrollProgress) * 0.06;
    const elapsed = globalThis.performance.now() * 0.001;

    // Inertial damping for manual drag
    if (!isDragging) {
      dragVelocityX *= 0.94;
      dragVelocityY *= 0.94;
      dragRotationX += dragVelocityX;
      dragRotationY += dragVelocityY;
    }

    // Base angles combined with scroll progress and interactive drag
    const basePitch = 0.22 + scrollProgress * 0.2 + dragRotationX;
    const baseYaw =
      -0.45 + scrollProgress * Math.PI * 2.1 + Math.sin(elapsed * 0.8) * 0.05 + dragRotationY;
    const baseRoll = Math.sin(scrollProgress * Math.PI) * 0.08;

    mainGroup.rotation.x = basePitch;
    mainGroup.rotation.y = baseYaw;
    mainGroup.rotation.z = baseRoll;

    // Gentle floating breathing motion
    mainGroup.position.y = -0.65 + Math.sin(elapsed * 1.4) * 0.04 + (scrollProgress - 0.5) * 0.18;

    // Gentle scale punch during scroll
    const scale = 1.0 + Math.sin(scrollProgress * Math.PI) * 0.12;
    mainGroup.scale.setScalar(scale);

    // Animate rising steam particles
    const posAttr = steamGeometry.attributes.position as BufferAttribute;
    const arr = posAttr.array as Float32Array;
    for (let i = 0; i < steamCount; i++) {
      const speed = steamSpeeds[i] ?? 0.01;
      const drift = steamDrifts[i] ?? 0;
      arr[i * 3 + 1] = (arr[i * 3 + 1] ?? 0) + speed;
      arr[i * 3] = (arr[i * 3] ?? 0) + Math.sin(elapsed * 2 + drift) * 0.003;
      arr[i * 3 + 2] = (arr[i * 3 + 2] ?? 0) + Math.cos(elapsed * 2 + drift) * 0.003;

      // Reset when particle drifts too high
      if ((arr[i * 3 + 1] ?? 0) > 3.3) {
        arr[i * 3 + 1] = 1.7 + Math.random() * 0.2;
        const angle = Math.random() * Math.PI * 2;
        const r = Math.random() * 0.7;
        arr[i * 3] = Math.cos(angle) * r;
        arr[i * 3 + 2] = Math.sin(angle) * r;
      }
    }
    posAttr.needsUpdate = true;

    renderer.render(scene, camera);
    frame = globalThis.requestAnimationFrame(render);
  };

  const resize = () => {
    const host = canvas.parentElement;
    if (!host) return;
    const width = Math.max(host.clientWidth, 1);
    const height = Math.max(host.clientHeight, 1);
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.render(scene, camera);
  };

  const observer = new ResizeObserver(resize);
  observer.observe(canvas.parentElement ?? canvas);

  const onVisibility = () => {
    visible = !globalThis.document.hidden;
    globalThis.cancelAnimationFrame(frame);
    if (visible) render();
  };
  globalThis.document.addEventListener("visibilitychange", onVisibility);

  resize();
  render();

  return {
    setScrollProgress(progress) {
      targetScrollProgress = Math.min(Math.max(progress, 0), 1);
    },
    destroy() {
      active = false;
      globalThis.cancelAnimationFrame(frame);
      observer.disconnect();
      globalThis.document.removeEventListener("visibilitychange", onVisibility);

      canvas.removeEventListener("mousedown", onPointerDown);
      window.removeEventListener("mousemove", onPointerMove);
      window.removeEventListener("mouseup", onPointerUp);
      canvas.removeEventListener("touchstart", onPointerDown);
      window.removeEventListener("touchmove", onPointerMove);
      window.removeEventListener("touchend", onPointerUp);

      cupGeometry.dispose();
      cupGoldGeometry.dispose();
      liquidGeometry.dispose();
      handleGeometry.dispose();
      saucerGeometry.dispose();
      saucerGoldGeometry.dispose();
      steamGeometry.dispose();

      ceramicMaterial.dispose();
      goldMaterial.dispose();
      latteArtTexture.dispose();
      coffeeMaterial.dispose();
      beanMaterial.dispose();
      steamMaterial.dispose();

      renderer.dispose();
      renderer.forceContextLoss();
    },
  };
}
