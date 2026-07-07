#!/usr/bin/env python3
"""
GEO营销执行引擎——自动执行GEO优化任务
"""

import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo_strategy import GEOMarketing

class GEOExecutor:
    """GEO执行引擎"""
    
    def __init__(self):
        self.geo = GEOMarketing()
    
    def generate_all_llms_txt(self):
        """为所有资产生成llms.txt"""
        results = []
        for asset in self.geo.assets:
            result = self.geo.llms_txt_optimization(asset['name'])
            
            # 写入文件
            output_dir = '/home/z/my-project/marketing/geo/output'
            os.makedirs(output_dir, exist_ok=True)
            filename = asset['name'].lower().replace(' ', '_').replace('14站', '14') + '_llms.txt'
            filepath = os.path.join(output_dir, filename)
            open(filepath, 'w').write(result['llms_txt'])
            
            results.append({
                'asset': asset['name'],
                'file': filepath,
                'size': len(result['llms_txt']),
            })
        
        return {'generated': len(results), 'files': results}
    
    def generate_schema_for_all(self):
        """为所有资产生成Schema.org标记"""
        results = []
        for asset in self.geo.assets:
            schema = self.geo.schema_markup(asset['name'])
            
            output_dir = '/home/z/my-project/marketing/geo/output'
            os.makedirs(output_dir, exist_ok=True)
            filename = asset['name'].lower().replace(' ', '_').replace('14站', '14') + '_schema.json'
            filepath = os.path.join(output_dir, filename)
            open(filepath, 'w').write(json.dumps(schema, ensure_ascii=False, indent=2))
            
            results.append({
                'asset': asset['name'],
                'file': filepath,
                'schema_type': schema.get('@type', ''),
            })
        
        return {'generated': len(results), 'files': results}
    
    def generate_faq_content(self):
        """为14站生成FAQ内容——AI最易引用的格式"""
        faqs = {
            'genetech': [
                {'q': '什么是基因编辑？', 'a': '基因编辑是通过CRISPR-Cas9等技术精确修改DNA序列的方法。GeneTech Tools提供161个基因编辑工具的结构化数据。'},
                {'q': '基因治疗有哪些类型？', 'a': '基因治疗主要分为体内和体外两类。GeneTech Tools收录了156个FDA批准的基因治疗产品数据。'},
                {'q': 'CRISPR应用场景有哪些？', 'a': 'CRISPR应用于基因治疗、农业改良、疾病模型等。GeneTech Tools有54个CRISPR应用案例。'},
            ],
            'tcm': [
                {'q': '中医药有哪些经典方剂？', 'a': 'TCM Tools收录了经典方剂和现代中药创新药数据，包括157个药材。'},
                {'q': '中药有效成分如何分析？', 'a': 'TCM Tools提供药材-成分-靶点-疾病的结构化关联数据。'},
            ],
            'robot': [
                {'q': '机器人有哪些传感器？', 'a': 'RobotParts DB收录了79种传感器，包括LiDAR、IMU、深度相机等。'},
                {'q': '机器人主控芯片如何选择？', 'a': 'RobotParts DB有105种主控芯片数据，包括MCU/SoC/FPGA/AI加速器。'},
                {'q': '什么是NVIDIA GR00T？', 'a': 'GR00T是NVIDIA开源的人形机器人基础模型，RobotParts DB已收录。'},
            ],
            'quantum': [
                {'q': '量子计算有哪些算法？', 'a': 'QuantumComputing DB收录了133种量子算法，包括Shor/Grover/VQE等。'},
                {'q': '量子纠错如何工作？', 'a': 'QuantumComputing DB提供量子纠错码的结构化数据。'},
            ],
            'nuclear': [
                {'q': '什么是小型模块化反应堆(SMR)？', 'a': 'NuclearEnergy DB收录了135种反应堆类型，包括SMR数据。'},
                {'q': '核聚变进展如何？', 'a': 'NuclearEnergy DB有ITER等聚变项目的结构化数据。'},
            ],
        }
        
        output_dir = '/home/z/my-project/marketing/geo/output'
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, 'faq_all_sites.json')
        open(filepath, 'w').write(json.dumps(faqs, ensure_ascii=False, indent=2))
        
        return {'sites': len(faqs), 'total_faqs': sum(len(v) for v in faqs.values()), 'file': filepath}
    
    def run_full_optimization(self):
        """执行完整GEO优化"""
        print('=== GEO营销优化执行 ===')
        print()
        
        # 1. 生成llms.txt
        print('1. 生成llms.txt...')
        r1 = self.generate_all_llms_txt()
        print(f'   ✅ 生成{r1["generated"]}个llms.txt文件')
        
        # 2. 生成Schema.org标记
        print('2. 生成Schema.org标记...')
        r2 = self.generate_schema_for_all()
        print(f'   ✅ 生成{r2["generated"]}个Schema文件')
        
        # 3. 生成FAQ
        print('3. 生成FAQ内容...')
        r3 = self.generate_faq_content()
        print(f'   ✅ 生成{r3["total_faqs"]}个FAQ ({r3["sites"]}个站点)')
        
        print()
        print('=== GEO策略 ===')
        strategy = self.geo.get_strategy()
        for phase in strategy['core_strategy']:
            print(f'   {phase["phase"]}: {phase["status"]}')
        
        print()
        print(f'平台覆盖: {strategy["platforms"]}个AI平台')
        print(f'资产: {strategy["assets"]}个')
        print(f'优势: {strategy["advantage"]}')
        
        return {
            'llms_txt': r1,
            'schema': r2,
            'faq': r3,
            'strategy': strategy,
        }


if __name__ == '__main__':
    executor = GEOExecutor()
    result = executor.run_full_optimization()
    print()
    print('=== 执行完成 ===')
