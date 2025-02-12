import * as THREE from 'three';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

let scene, camera, renderer, controls, bed;
let importedObjects = [];

init();

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xbbbbbb);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 100, 200);

    renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.screenSpacePanning = false;
    controls.mouseButtons = {
        LEFT: THREE.MOUSE.ROTATE,
        MIDDLE: THREE.MOUSE.DOLLY,
    };

    addPrintBed();
    addLighting();

    document.getElementById('fileInput').addEventListener('change', handleFile);
    document.getElementById('jsonInput').addEventListener('change', handleJson);
    document.getElementById('clearButton').addEventListener('click', clearScene);

    window.addEventListener('resize', onWindowResize);
    window.addEventListener('keydown', handleKeyDown);

    animate();
}

function handleKeyDown(event) {
    switch (event.key.toLowerCase()) {
        case 'b': // Reset to default position
            controls.reset();
            camera.position.set(0, 100, 200);
            break;
        case 'z': // Zoom out to fit scene
            zoomToScene();
            break;
        case '0': // Isometric view
            camera.position.set(150, 150, 150);
            break;
        case '1': // Top-down view
            camera.position.set(0, 200, 0);
            break;
        case '2': // Bottom-up view
            camera.position.set(0, 0, 250);
            break;
        case '3': // Front view
            camera.position.set(0, 100, 200);
            break;
        case '4': // Back view
            camera.position.set(0, 100, -200);
            break;
        case '5': // Left view
            camera.position.set(-200, 100, 0);
            break;
        case '6': // Right view
            camera.position.set(200, 100, 0);
            break;
        case 'i': // Zoom in
            camera.position.addScaledVector(camera.getWorldDirection(new THREE.Vector3()), -10);
            break;
        case 'o': // Zoom out
            camera.position.addScaledVector(camera.getWorldDirection(new THREE.Vector3()), 10);
            break;
    }
    controls.update();
}

function zoomToScene() {
    const box = new THREE.Box3().setFromObject(scene);
    if (!box.isEmpty()) {
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3()).length();
        camera.position.set(center.x, center.y + size, center.z + size);
        controls.target.copy(center);
    }
    controls.update();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

function addPrintBed() {
    const bedSize = 250;
    const bedHeight = 2;
    const bedColor = 0x333333;
    const lineColor = 0x666666;
    const smallLineColor = 0x555555;

    const bedGeometry = new THREE.BoxGeometry(bedSize, bedHeight, bedSize);
    const bedMaterial = new THREE.MeshStandardMaterial({
        color: 0x333333,
        roughness: 1,
        metalness: 0.1
    });

    bed = new THREE.Mesh(bedGeometry, bedMaterial);
    bed.position.y = -bedHeight / 2;
    scene.add(bed);

    const gridSize = 50;
    const gridHelper = new THREE.GridHelper(bedSize, bedSize / gridSize, lineColor, lineColor);
    gridHelper.position.y = 0.01;
    gridHelper.material.linewidth = 2;
    scene.add(gridHelper);

    const smallGridSize = 10;
    const smallGridHelper = new THREE.GridHelper(bedSize, bedSize / smallGridSize, smallLineColor, smallLineColor);
    smallGridHelper.position.y = 0;
    smallGridHelper.material.linewidth = 1;
    scene.add(smallGridHelper);

    const borderMaterial = new THREE.LineBasicMaterial({ color: lineColor, linewidth: 10 });
    const borderGeometry = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(-bedSize / 2, 0.02, -bedSize / 2),
        new THREE.Vector3(bedSize / 2, 0.02, -bedSize / 2),
        new THREE.Vector3(bedSize / 2, 0.02, bedSize / 2),
        new THREE.Vector3(-bedSize / 2, 0.02, bedSize / 2),
        new THREE.Vector3(-bedSize / 2, 0.02, -bedSize / 2)
    ]);
    const border = new THREE.Line(borderGeometry, borderMaterial);
    scene.add(border);

    const axisSize = 12;

    // X axis (red)
    const xAxisMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 });
    const xAxisGeometry = new THREE.BoxGeometry(axisSize, 1, 1);
    const xAxis = new THREE.Mesh(xAxisGeometry, xAxisMaterial);
    xAxis.position.set(axisSize / 2 - bedSize / 2, 0.5, bedSize / 2);
    scene.add(xAxis);

    // Y axis (green)
    const yAxisMaterial = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
    const yAxisGeometry = new THREE.BoxGeometry(1, 1, axisSize);
    const yAxis = new THREE.Mesh(yAxisGeometry, yAxisMaterial);
    yAxis.position.set(-bedSize / 2, 0.5, bedSize / 2 - axisSize / 2);
    scene.add(yAxis);

    // Z axis (blue)
    const zAxisMaterial = new THREE.MeshStandardMaterial({ color: 0x0000ff });
    const zAxisGeometry = new THREE.BoxGeometry(1, axisSize, 1);
    const zAxis = new THREE.Mesh(zAxisGeometry, zAxisMaterial);
    zAxis.position.set(-bedSize / 2, axisSize / 2, bedSize / 2);
    scene.add(zAxis);
}

function addLighting() {
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(10, 10, 10);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x404040));
}

function handleFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        const loader = new STLLoader();
        const geometry = loader.parse(e.target.result);

        geometry.computeBoundingBox();
        const bbox = geometry.boundingBox;
        const center = new THREE.Vector3();
        bbox.getCenter(center);

        const size = new THREE.Vector3();
        bbox.getSize(size);
        const minY = bbox.min.y;

        const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
        const mesh = new THREE.Mesh(geometry, material);

        mesh.position.set(-center.x, 0, -center.z - minY);
        mesh.rotation.x = Math.PI / 2;
        mesh.scale.set(1, 1, -1);

        scene.add(mesh);
        objectInfo(file.name, mesh);

        console.log('STL file imported:', mesh);
    };
    reader.readAsArrayBuffer(file);
}

function objectInfo(name, mesh) {
    const objectInfo = {
        name: name,
        position: { x: mesh.position.x, y: mesh.position.y, z: mesh.position.z },
        rotation: { x: THREE.MathUtils.radToDeg(mesh.rotation.x), y: THREE.MathUtils.radToDeg(mesh.rotation.y), z: THREE.MathUtils.radToDeg(mesh.rotation.z) },
        scale: { x: mesh.scale.x, y: mesh.scale.y, z: mesh.scale.z}
    };

    importedObjects.push({ mesh, objectInfo });

    // Debugging statement
    console.log('Object created:', objectInfo);
}

function handleJson(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        const layers = JSON.parse(e.target.result);
        drawLayers(layers);
    };
    reader.readAsText(file);
}

function drawLayers(layers) {
    const vertices = [];

    layers.forEach((layer, i) => {
        const zHeight = i * 0.2;
        layer.forEach(p => {
            vertices.push(p[0], zHeight, p[1]);
        });
    });

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));

    const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
    const lines = new THREE.LineSegments(geometry, material);

    importedObjects.push(lines);
    scene.add(lines);
}

function clearScene() {
    importedObjects.forEach(obj => scene.remove(obj.mesh || obj));
    importedObjects = [];
    console.log('Scene cleared');
}