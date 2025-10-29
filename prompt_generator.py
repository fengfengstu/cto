"""
AI图像生成提示词变奏生成器
基于金字塔结构和MECE法则生成提示词变奏
"""

import random
from typing import List, Dict, Any, Optional
from prompt_pyramid import (
    PROMPT_PYRAMID, 
    VARIATION_STRATEGIES, 
    QUALITY_KEYWORDS,
    NEGATIVE_PROMPTS
)


class PromptGenerator:
    """提示词生成器"""
    
    def __init__(self):
        self.pyramid = PROMPT_PYRAMID
        self.strategies = VARIATION_STRATEGIES
        self.quality_keywords = QUALITY_KEYWORDS
        self.negative_prompts = NEGATIVE_PROMPTS
    
    def get_pyramid_structure(self) -> Dict[str, Any]:
        """获取金字塔结构"""
        return self.pyramid
    
    def get_all_dimensions(self) -> List[str]:
        """获取所有一级维度"""
        return list(self.pyramid["结构"]["一级维度"].keys())
    
    def get_dimension_info(self, dimension: str) -> Dict[str, Any]:
        """获取指定维度的详细信息"""
        return self.pyramid["结构"]["一级维度"].get(dimension, {})
    
    def get_subdimensions(self, dimension: str) -> List[str]:
        """获取指定维度的所有子维度"""
        dim_info = self.get_dimension_info(dimension)
        if "子维度" in dim_info:
            return list(dim_info["子维度"].keys())
        return []
    
    def get_options(self, dimension: str, subdimension: str) -> Dict[str, List[str]]:
        """获取指定子维度的所有选项"""
        dim_info = self.get_dimension_info(dimension)
        if "子维度" in dim_info:
            return dim_info["子维度"].get(subdimension, {})
        return {}
    
    def random_element_from_dimension(self, dimension: str) -> str:
        """从指定维度随机选择一个元素"""
        subdimensions = self.get_subdimensions(dimension)
        if not subdimensions:
            return ""
        
        subdim = random.choice(subdimensions)
        options = self.get_options(dimension, subdim)
        
        if options:
            category = random.choice(list(options.keys()))
            elements = options[category]
            if elements:
                return random.choice(elements)
        return ""
    
    def generate_base_prompt(self, 
                           subject: str = "",
                           style: str = "",
                           environment: str = "",
                           technical: str = "",
                           atmosphere: str = "",
                           innovation: str = "") -> str:
        """生成基础提示词"""
        components = []
        
        if subject:
            components.append(subject)
        if style:
            components.append(style)
        if environment:
            components.append(environment)
        if technical:
            components.append(technical)
        if atmosphere:
            components.append(atmosphere)
        if innovation:
            components.append(innovation)
        
        return "，".join(components)
    
    def generate_random_prompt(self, 
                             include_quality: bool = True,
                             dimensions_count: int = 6) -> Dict[str, Any]:
        """生成随机提示词"""
        dimensions = self.get_all_dimensions()
        selected_dims = random.sample(dimensions, min(dimensions_count, len(dimensions)))
        
        prompt_parts = {}
        for dim in selected_dims:
            element = self.random_element_from_dimension(dim)
            if element:
                prompt_parts[dim] = element
        
        base_prompt = self.generate_base_prompt(
            subject=prompt_parts.get("1.主体层", ""),
            style=prompt_parts.get("2.风格层", ""),
            environment=prompt_parts.get("3.环境层", ""),
            technical=prompt_parts.get("4.技术层", ""),
            atmosphere=prompt_parts.get("5.氛围层", ""),
            innovation=prompt_parts.get("6.创新层", "")
        )
        
        full_prompt = base_prompt
        if include_quality:
            quality_words = random.sample(
                self.quality_keywords["通用质量词"], 
                min(3, len(self.quality_keywords["通用质量词"]))
            )
            full_prompt = "，".join(quality_words) + "，" + full_prompt
        
        return {
            "提示词": full_prompt,
            "维度分解": prompt_parts,
            "包含质量词": include_quality
        }
    
    def generate_variations(self, 
                          base_prompt: str,
                          strategy: str = "单维度变奏",
                          count: int = 5) -> List[Dict[str, Any]]:
        """基于策略生成变奏"""
        variations = []
        
        if strategy == "单维度变奏":
            variations = self._generate_single_dimension_variations(base_prompt, count)
        elif strategy == "跨维度组合":
            variations = self._generate_cross_dimension_variations(base_prompt, count)
        elif strategy == "对比变奏":
            variations = self._generate_contrast_variations(base_prompt, count)
        elif strategy == "渐进变奏":
            variations = self._generate_progressive_variations(base_prompt, count)
        elif strategy == "极端变奏":
            variations = self._generate_extreme_variations(base_prompt, count)
        else:  # 混合实验
            variations = self._generate_mixed_variations(base_prompt, count)
        
        return variations
    
    def _generate_single_dimension_variations(self, base: str, count: int) -> List[Dict[str, Any]]:
        """单维度变奏"""
        variations = []
        dimensions = self.get_all_dimensions()
        
        for i in range(count):
            dim = random.choice(dimensions)
            element = self.random_element_from_dimension(dim)
            variation = f"{base}，{element}"
            variations.append({
                "变奏": variation,
                "策略": "单维度变奏",
                "维度": dim,
                "元素": element
            })
        
        return variations
    
    def _generate_cross_dimension_variations(self, base: str, count: int) -> List[Dict[str, Any]]:
        """跨维度组合变奏"""
        variations = []
        dimensions = self.get_all_dimensions()
        
        for i in range(count):
            selected_dims = random.sample(dimensions, min(3, len(dimensions)))
            elements = [self.random_element_from_dimension(dim) for dim in selected_dims]
            elements = [e for e in elements if e]
            
            variation = f"{base}，{'，'.join(elements)}"
            variations.append({
                "变奏": variation,
                "策略": "跨维度组合",
                "维度": selected_dims,
                "元素": elements
            })
        
        return variations
    
    def _generate_contrast_variations(self, base: str, count: int) -> List[Dict[str, Any]]:
        """对比变奏"""
        contrast_pairs = [
            ("古代", "未来"),
            ("自然", "人造"),
            ("明亮", "黑暗"),
            ("写实", "抽象"),
            ("微观", "宏观"),
            ("温暖", "冷峻"),
            ("简约", "华丽"),
            ("静止", "动态")
        ]
        
        variations = []
        for i in range(count):
            pair = random.choice(contrast_pairs)
            element = random.choice(pair)
            variation = f"{base}，{element}风格"
            variations.append({
                "变奏": variation,
                "策略": "对比变奏",
                "对比组": pair,
                "选择": element
            })
        
        return variations
    
    def _generate_progressive_variations(self, base: str, count: int) -> List[Dict[str, Any]]:
        """渐进变奏"""
        progressive_sequences = [
            ["清晨", "上午", "正午", "下午", "黄昏", "夜晚"],
            ["完整", "轻微破损", "破损", "严重破碎", "废墟"],
            ["写实", "半写实", "风格化", "抽象", "极简"],
            ["平静", "微动", "活跃", "激烈", "爆发"],
            ["微观", "近景", "中景", "远景", "全景"]
        ]
        
        variations = []
        sequence = random.choice(progressive_sequences)
        
        for i in range(min(count, len(sequence))):
            variation = f"{base}，{sequence[i]}"
            variations.append({
                "变奏": variation,
                "策略": "渐进变奏",
                "序列": sequence,
                "阶段": i + 1,
                "当前": sequence[i]
            })
        
        return variations
    
    def _generate_extreme_variations(self, base: str, count: int) -> List[Dict[str, Any]]:
        """极端变奏"""
        extreme_modifiers = [
            "极度夸张的", "极简主义", "极致细节", "极端对比",
            "超现实", "极度扭曲", "无限重复", "完全抽象",
            "纯粹色彩", "纯黑白", "爆炸性", "绝对静止"
        ]
        
        variations = []
        for i in range(count):
            modifier = random.choice(extreme_modifiers)
            variation = f"{modifier}，{base}"
            variations.append({
                "变奏": variation,
                "策略": "极端变奏",
                "修饰词": modifier
            })
        
        return variations
    
    def _generate_mixed_variations(self, base: str, count: int) -> List[Dict[str, Any]]:
        """混合实验变奏"""
        variations = []
        
        for i in range(count):
            elements = []
            dimensions = random.sample(self.get_all_dimensions(), 
                                     random.randint(2, 4))
            
            for dim in dimensions:
                element = self.random_element_from_dimension(dim)
                if element:
                    elements.append(element)
            
            random.shuffle(elements)
            variation = f"{base}，{'，'.join(elements)}"
            
            variations.append({
                "变奏": variation,
                "策略": "混合实验",
                "维度": dimensions,
                "元素": elements
            })
        
        return variations
    
    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """分析提示词，识别其中的维度元素"""
        analysis = {
            "原始提示词": prompt,
            "识别的元素": {},
            "覆盖维度": [],
            "建议补充": []
        }
        
        for dimension in self.get_all_dimensions():
            subdimensions = self.get_subdimensions(dimension)
            found_elements = []
            
            for subdim in subdimensions:
                options = self.get_options(dimension, subdim)
                for category, elements in options.items():
                    for element in elements:
                        if element in prompt:
                            found_elements.append({
                                "子维度": subdim,
                                "类别": category,
                                "元素": element
                            })
            
            if found_elements:
                analysis["识别的元素"][dimension] = found_elements
                analysis["覆盖维度"].append(dimension)
        
        all_dimensions = set(self.get_all_dimensions())
        covered_dimensions = set(analysis["覆盖维度"])
        missing_dimensions = all_dimensions - covered_dimensions
        
        for dim in missing_dimensions:
            analysis["建议补充"].append({
                "维度": dim,
                "描述": self.get_dimension_info(dim).get("描述", ""),
                "示例": self.random_element_from_dimension(dim)
            })
        
        return analysis
    
    def get_quality_prompt(self, level: str = "通用") -> str:
        """获取质量提示词"""
        if level == "通用":
            keywords = self.quality_keywords.get("通用质量词", [])
        elif level == "艺术":
            keywords = self.quality_keywords.get("艺术质量词", [])
        else:
            keywords = self.quality_keywords.get("技术质量词", [])
        
        selected = random.sample(keywords, min(3, len(keywords)))
        return "，".join(selected)
    
    def get_negative_prompt(self, category: str = "全部") -> str:
        """获取负面提示词"""
        if category == "全部":
            all_negatives = []
            for neg_list in self.negative_prompts.values():
                all_negatives.extend(neg_list)
            selected = random.sample(all_negatives, min(10, len(all_negatives)))
        else:
            negatives = self.negative_prompts.get(f"{category}负面词", [])
            selected = random.sample(negatives, min(5, len(negatives)))
        
        return "，".join(selected)
    
    def generate_complete_prompt_set(self, base_idea: str) -> Dict[str, Any]:
        """生成完整的提示词集合"""
        analysis = self.analyze_prompt(base_idea)
        
        enriched_prompt = base_idea
        if analysis["建议补充"]:
            supplements = [item["示例"] for item in analysis["建议补充"][:3]]
            enriched_prompt = f"{base_idea}，{'，'.join(supplements)}"
        
        quality = self.get_quality_prompt("通用")
        negative = self.get_negative_prompt("全部")
        
        variations = {}
        for strategy in ["单维度变奏", "跨维度组合", "对比变奏", "渐进变奏", "极端变奏", "混合实验"]:
            variations[strategy] = self.generate_variations(enriched_prompt, strategy, 3)
        
        return {
            "原始想法": base_idea,
            "分析结果": analysis,
            "增强提示词": enriched_prompt,
            "完整正向提示词": f"{quality}，{enriched_prompt}",
            "负向提示词": negative,
            "变奏方案": variations,
            "统计": {
                "覆盖维度数": len(analysis["覆盖维度"]),
                "建议补充数": len(analysis["建议补充"]),
                "总变奏数": sum(len(v) for v in variations.values())
            }
        }
