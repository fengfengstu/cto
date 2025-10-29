#!/usr/bin/env python3
"""
AI图像生成提示词变奏创意助手 - 命令行版本
"""

import sys
import argparse
import json
from prompt_generator import PromptGenerator


def print_header(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_section(text):
    """打印章节"""
    print(f"\n{'─' * 60}")
    print(f"  {text}")
    print('─' * 60)


def list_dimensions(generator):
    """列出所有维度"""
    print_header("📖 金字塔结构 - 六大维度")
    
    dimensions = generator.get_all_dimensions()
    
    for dim in dimensions:
        dim_info = generator.get_dimension_info(dim)
        print(f"\n{dim}")
        print(f"  描述：{dim_info.get('描述', '')}")
        
        subdimensions = generator.get_subdimensions(dim)
        print(f"  子维度：{', '.join(subdimensions)}")


def show_dimension_detail(generator, dimension):
    """显示维度详情"""
    print_header(f"📖 维度详情：{dimension}")
    
    dim_info = generator.get_dimension_info(dimension)
    print(f"描述：{dim_info.get('描述', '')}\n")
    
    subdimensions = generator.get_subdimensions(dimension)
    
    for subdim in subdimensions:
        print_section(subdim)
        options = generator.get_options(dimension, subdim)
        
        for category, elements in options.items():
            print(f"\n{category}:")
            for element in elements:
                print(f"  • {element}")


def generate_random(generator, count=1, include_quality=True, dimensions_count=4):
    """生成随机提示词"""
    print_header("✨ 随机提示词生成")
    
    for i in range(count):
        if count > 1:
            print(f"\n{'━' * 60}")
            print(f"  提示词 #{i + 1}")
            print('━' * 60)
        
        result = generator.generate_random_prompt(
            include_quality=include_quality,
            dimensions_count=dimensions_count
        )
        
        print("\n📝 生成的提示词：")
        print(f"\n{result['提示词']}\n")
        
        print("🔍 维度分解：")
        for dim, element in result["维度分解"].items():
            print(f"  • {dim}: {element}")


def generate_variations(generator, base_prompt, strategy="单维度变奏", count=5):
    """生成变奏"""
    print_header(f"🔄 提示词变奏 - {strategy}")
    
    print(f"基础提示词：\n{base_prompt}\n")
    
    variations = generator.generate_variations(base_prompt, strategy, count)
    
    for idx, var in enumerate(variations, 1):
        print(f"\n{'─' * 60}")
        print(f"变奏 #{idx}")
        print('─' * 60)
        print(f"\n{var['变奏']}\n")
        
        print("变奏信息：")
        for key, value in var.items():
            if key != "变奏":
                print(f"  • {key}: {value}")


def analyze_prompt(generator, prompt):
    """分析提示词"""
    print_header("🔍 提示词分析")
    
    print(f"原始提示词：\n{prompt}\n")
    
    analysis = generator.analyze_prompt(prompt)
    
    print_section("统计信息")
    print(f"覆盖维度数：{len(analysis['覆盖维度'])}")
    print(f"建议补充数：{len(analysis['建议补充'])}")
    
    if analysis["识别的元素"]:
        print_section("✅ 已识别的元素")
        for dim, elements in analysis["识别的元素"].items():
            print(f"\n{dim}:")
            for elem in elements:
                print(f"  • {elem['子维度']} / {elem['类别']}: {elem['元素']}")
    
    if analysis["建议补充"]:
        print_section("💡 建议补充的维度")
        for sugg in analysis["建议补充"]:
            print(f"\n{sugg['维度']}:")
            print(f"  描述：{sugg['描述']}")
            print(f"  示例：{sugg['示例']}")


def generate_complete(generator, base_idea, output_file=None):
    """生成完整方案"""
    print_header("📦 完整提示词方案生成")
    
    print(f"核心创意：{base_idea}\n")
    print("正在生成完整方案...")
    
    result = generator.generate_complete_prompt_set(base_idea)
    
    print("\n✅ 生成完成！\n")
    
    print_section("📊 方案统计")
    print(f"覆盖维度数：{result['统计']['覆盖维度数']}")
    print(f"补充建议数：{result['统计']['建议补充数']}")
    print(f"总变奏数：{result['统计']['总变奏数']}")
    
    print_section("📝 完整提示词")
    print("\n正向提示词：")
    print(f"\n{result['完整正向提示词']}\n")
    
    print("负向提示词：")
    print(f"\n{result['负向提示词']}\n")
    
    print_section("🎨 变奏方案预览")
    for strategy_name, variations in result["变奏方案"].items():
        print(f"\n{strategy_name} ({len(variations)}个变奏):")
        for idx, var in enumerate(variations, 1):
            print(f"  {idx}. {var['变奏']}")
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n💾 完整方案已保存到：{output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="AI图像生成提示词变奏创意助手 - 命令行版本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  # 列出所有维度
  python cli.py --list-dimensions
  
  # 查看某个维度详情
  python cli.py --show-dimension "1.主体层"
  
  # 生成随机提示词
  python cli.py --random --count 3
  
  # 生成变奏
  python cli.py --variations "一位穿汉服的少女" --strategy "对比变奏" --count 5
  
  # 分析提示词
  python cli.py --analyze "赛博朋克风格的猫，霓虹灯光"
  
  # 生成完整方案
  python cli.py --complete "未来城市" --output result.json
        """
    )
    
    parser.add_argument('--list-dimensions', action='store_true',
                       help='列出所有维度')
    
    parser.add_argument('--show-dimension', metavar='DIM',
                       help='显示指定维度的详细信息')
    
    parser.add_argument('--random', action='store_true',
                       help='生成随机提示词')
    
    parser.add_argument('--variations', metavar='PROMPT',
                       help='为指定提示词生成变奏')
    
    parser.add_argument('--analyze', metavar='PROMPT',
                       help='分析指定提示词')
    
    parser.add_argument('--complete', metavar='IDEA',
                       help='生成完整方案')
    
    parser.add_argument('--strategy', default='单维度变奏',
                       choices=['单维度变奏', '跨维度组合', '对比变奏', 
                               '渐进变奏', '极端变奏', '混合实验'],
                       help='变奏策略（默认：单维度变奏）')
    
    parser.add_argument('--count', type=int, default=5,
                       help='生成数量（默认：5）')
    
    parser.add_argument('--dimensions-count', type=int, default=4,
                       help='随机生成时包含的维度数（默认：4）')
    
    parser.add_argument('--no-quality', action='store_true',
                       help='随机生成时不包含质量词')
    
    parser.add_argument('--output', '-o', metavar='FILE',
                       help='输出文件路径（仅用于--complete）')
    
    args = parser.parse_args()
    
    generator = PromptGenerator()
    
    if args.list_dimensions:
        list_dimensions(generator)
    
    elif args.show_dimension:
        show_dimension_detail(generator, args.show_dimension)
    
    elif args.random:
        generate_random(
            generator, 
            count=args.count,
            include_quality=not args.no_quality,
            dimensions_count=args.dimensions_count
        )
    
    elif args.variations:
        generate_variations(
            generator,
            args.variations,
            strategy=args.strategy,
            count=args.count
        )
    
    elif args.analyze:
        analyze_prompt(generator, args.analyze)
    
    elif args.complete:
        generate_complete(generator, args.complete, args.output)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
