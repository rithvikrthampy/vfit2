from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import subprocess
import datetime
from pathlib import Path

def index(request):
    """Gallery of demo shirts (thumbnails)"""
    return render(request, "index.html")

def api_list_shirts(request):
    """API endpoint to list available shirts"""
    shirts_data = []
    for i in range(5):  # shirt0 to shirt4
        shirts_data.append({
            "img_id": i,
            "front_url": f"/media/shirts/shirt{i}.jpg",
            "back_url": f"/media/shirts/shirt{i}_b.jpg"
        })
    return JsonResponse({"items": shirts_data})

def api_run_pix2surf(request):
    """API endpoint to run pix2surf processing"""
    img_id = request.GET.get('img_id', '0')
    pose_id = request.GET.get('pose_id', '0')
    low_type = request.GET.get('low_type', 'shorts')
    
    # Create timestamped run directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = settings.BASE_DIR / "data" / "media" / f"run_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    
    # Run pix2surf processing
    pix2surf_dir = settings.BASE_DIR / "pix2surf"
    cmd = [
        "python", "demo.py",
        "--img_id", str(img_id),
        "--pose_id", str(pose_id),
        "--low_type", low_type,
        "--output", str(run_dir / "textures"),
        "--video", str(run_dir / "video")
    ]
    
    try:
        # Change to pix2surf directory and run
        result = subprocess.run(cmd, cwd=pix2surf_dir, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            return JsonResponse({"error": f"Processing failed: {result.stderr}"}, status=500)
        
        # Copy mesh files from pix2surf test_data to run directory
        import shutil
        mesh_source_dir = pix2surf_dir / "test_data" / "meshes" / low_type
        for mesh_name in ["body_0.obj", "upper_0.obj", "lower_0.obj"]:
            source_file = mesh_source_dir / mesh_name.replace("_0", f"_{pose_id}")
            dest_file = run_dir / mesh_name
            if source_file.exists():
                shutil.copy2(source_file, dest_file)
        
        # Collect generated frames
        video_dir = run_dir / "video"
        frames = []
        if video_dir.exists():
            for frame_file in sorted(video_dir.glob("im_*.png")):
                frames.append(f"/media/run_{timestamp}/video/{frame_file.name}")
        
        # Set mesh file paths
        mesh_files = {
            "body": f"/media/run_{timestamp}/body_0.obj",
            "upper": f"/media/run_{timestamp}/upper_0.obj", 
            "lower": f"/media/run_{timestamp}/lower_0.obj"
        }
        
        # Copy body texture to run directory for consistency
        body_texture_source = pix2surf_dir / "test_data" / "images" / "body_tex" / "body_tex.jpg"
        body_texture_dest = run_dir / "textures" / "body_tex.jpg"
        if body_texture_source.exists():
            shutil.copy2(body_texture_source, body_texture_dest)
        
        # Set texture file paths - all from the same run directory
        texture_files = {
            "body": f"/media/run_{timestamp}/textures/body_tex.jpg",
            "up": f"/media/run_{timestamp}/textures/up.jpg",
            "low": f"/media/run_{timestamp}/textures/low.jpg"
        }
        
        return JsonResponse({
            "success": True,
            "run_id": f"run_{timestamp}",
            "meshes": mesh_files,
            "textures": texture_files,
            "frames": frames,
            "img_id": int(img_id),
            "pose_id": int(pose_id),
            "low_type": low_type
        })
        
    except subprocess.TimeoutExpired:
        return JsonResponse({"error": "Processing timed out"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def viewer_page(request):
    """Three.js viewer page; reads sessionStorage set by index page"""
    return render(request, "viewer.html")

# Keep old function for backward compatibility
def viewer(request):
    return viewer_page(request)

def api_run(request, img_id: int):
    """Legacy API endpoint - redirects to new processing endpoint"""
    return api_run_pix2surf(request)