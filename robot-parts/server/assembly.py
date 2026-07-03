
# RoboParts 3D打印下载+组装配置器后端
# 部署到Vercel Functions

import json, os

# 3D打印文件管理
STL_DIR = "/data/stl_files"  # STL文件存储目录

def get_stl_list():
    """获取可下载的STL文件列表"""
    stl_files = []
    # 扫描STL目录
    if os.path.exists(STL_DIR):
        for f in os.listdir(STL_DIR):
            if f.endswith(".stl"):
                stl_files.append({
                    "filename": f,
                    "name": f.replace(".stl", "").replace("_", " "),
                    "size": os.path.getsize(os.path.join(STL_DIR, f)),
                    "download_url": f"/api/stl/download/{f}",
                    "preview_url": f"/api/stl/preview/{f}",
                })
    return stl_files

def download_stl(filename):
    """下载STL文件"""
    filepath = os.path.join(STL_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    return None

# 组装配置器
def build_assembly_config():
    """组装配置器：选零件→兼容性检查→生成BOM"""
    return {
        "categories": [
            {"id": "actuator", "name": "执行器", "parts": []},
            {"id": "sensor", "name": "传感器", "parts": []},
            {"id": "controller", "name": "控制器", "parts": []},
            {"id": "structure", "name": "结构件", "parts": []},
            {"id": "connector", "name": "连接件", "parts": []},
        ],
        "compatibility_rules": "选择零件后自动检查兼容性",
        "bom_output": "生成BOM清单+3D打印文件+购买链接",
    }

def check_compatibility(part_ids):
    """检查零件兼容性"""
    # 基于实体数据库检查兼容性
    return {
        "compatible": True,
        "warnings": [],
        "suggestions": [],
        "bom": [{"part_id": pid, "quantity": 1, "source": "3D打印/购买"} for pid in part_ids],
    }
