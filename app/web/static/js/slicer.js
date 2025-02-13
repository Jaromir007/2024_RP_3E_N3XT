import * as THREE from 'three';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

class PrintBed {
    constructor(size, height) {
        this.size = size;
        this.height = height;

        this.color = 0x131313;
        this.lineColor = 0x666666;
        this.smallLineColor = 0x555555;

        this.gridSize = 50;
        this.smallGridSize = 10;

        this.axisSize = 10;

        this.xAxis = null;
        this.yAxis = null;  
        this.zAxis = null;

        this.bed = null;
        this.gridHelper = null;
        this.smallGridHelper = null;

        this.init();
    }

    init() {
        const geometry = new THREE.BoxGeometry(this.size, this.height, this.size);
        const material = new THREE.MeshStandardMaterial({
            color: this.color,
            roughness: 1,
            metalness: 0.1
        });
    
        this.bed = new THREE.Mesh(geometry, material);
        this.bed.position.y = -this.height / 2;
    
        this.gridHelper = new THREE.GridHelper(this.size, this.size / this.gridSize, this.lineColor, this.lineColor);
        this.gridHelper.position.y = 0.01;
        this.gridHelper.material.linewidth = 2;
    
        this.smallGridHelper = new THREE.GridHelper(this.size, this.size / this.smallGridSize, this.smallLineColor, this.smallLineColor);
        this.smallGridHelper.position.y = 0;
        this.smallGridHelper.material.linewidth = 1;
    
         // X axis (red)
         const xAxisMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 });
         const xAxisGeometry = new THREE.BoxGeometry(this.axisSize, 1, 1);
         this.xAxis = new THREE.Mesh(xAxisGeometry, xAxisMaterial);
         this.xAxis.position.set(this.axisSize / 2 - this.size / 2, 0.5, this.size / 2);
     
         // Y axis (green)
         const yAxisMaterial = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
         const yAxisGeometry = new THREE.BoxGeometry(1, 1, this.axisSize);
         this.yAxis = new THREE.Mesh(yAxisGeometry, yAxisMaterial);
         this.yAxis.position.set(-this.size / 2, 0.5, this.size / 2 - this.axisSize / 2);
     
         // Z axis (blue)
         const zAxisMaterial = new THREE.MeshStandardMaterial({ color: 0x0000ff });
         const zAxisGeometry = new THREE.BoxGeometry(1, this.axisSize, 1);
         this.zAxis = new THREE.Mesh(zAxisGeometry, zAxisMaterial);
         this.zAxis.position.set(-this.size / 2, this.axisSize / 2, this.size / 2);
    }

    render() {
        scene.add(this.bed);
        scene.add(this.gridHelper);
        scene.add(this.smallGridHelper);
        scene.add(this.xAxis);
        scene.add(this.yAxis);
        scene.add(this.zAxis);
    }
}


class Light {
    constructor() {
        this.color = 0xffffff;
        this.position = { x: 100, y: 100, z: 100 };
        this.light = new THREE.DirectionalLight(0xffffff, 0.3);
        this.hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.8);

        this.init();
    }

    init() {
        this.light.position.set(this.position.x, this.position.y, this.position.z);
        this.hemisphereLight.position.set(this.position.x, this.position.y, this.position.z);
    }

    setPosition(x, y, z) {
        this.position = { x, y, z };
    }

    render() {
        scene.add(this.light);
        scene.add(this.hemisphereLight);
    }
}

let scene, camera, renderer, controls, printBed, light;
let imported = [];

init();

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xbbbbbb);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 100, 200);

    const slicerCanvas = document.getElementById("slicerCanvas");
    renderer = new THREE.WebGLRenderer({
        antialias: true,
        powerPreference: "high-performance",
        canvas: slicerCanvas
    });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.screenSpacePanning = false;
    controls.mouseButtons = {
        LEFT: THREE.MOUSE.ROTATE,
        MIDDLE: THREE.MOUSE.DOLLY,
        RIGHT: THREE.MOUSE.PAN 
    };

    printBed = new PrintBed(200, 1);
    light = new Light();

    printBed.render();
    light.render(); 

    document.getElementById('fileInput').addEventListener('change', loadSTL);
    document.getElementById('jsonInput').addEventListener('change', loadJson);
    document.getElementById('clearButton').addEventListener('click', clearScene);

    window.addEventListener('resize', onWindowResize);
    window.addEventListener('keydown', handleKeyDown);

    animate();
}

function handleKeyDown(event) {
    switch (event.key.toLowerCase()) {
        case 'b': // Reset 
            controls.reset();
            camera.position.set(0, 100, 200);
            break;
        case 'z': // Zoom out 
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


function loadSTL(event) {
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

        geometry.translate(-center.x, -center.y, -center.z);

        const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
        const mesh = new THREE.Mesh(geometry, material);

        mesh.rotation.set(-Math.PI / 2, 0, 0);

        mesh.position.y = -bbox.min.z;

        scene.add(mesh);
        imported.push(mesh);

        console.log('STL file imported:', mesh);
    };
    reader.readAsArrayBuffer(file);
}

function loadJson(event) {
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

    imported.push(lines);
    scene.add(lines);
}

function clearScene() {
    imported.forEach(mesh => {
        if (mesh) {
            scene.remove(mesh);
            mesh.geometry.dispose();
            if (Array.isArray(mesh.material)) {
                mesh.material.forEach(mat => mat.dispose());
            } else {
                mesh.material.dispose();
            }
        } else {
            scene.remove(mesh);
        }
    });

    imported = [];

    console.log('Scene cleared');

    document.getElementById('fileInput').value = "";
    document.getElementById('jsonInput').value = "";

    renderer.render(scene, camera);
}
