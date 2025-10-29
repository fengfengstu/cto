"""
AI图像生成提示词变奏创意助手 - Web界面
基于金字塔理论和MECE法则的全中文提示词变奏系统
"""

import streamlit as st
import json
from prompt_generator import PromptGenerator
from prompt_pyramid import PROMPT_PYRAMID, VARIATION_STRATEGIES


def main():
    st.set_page_config(
        page_title="AI提示词变奏创意助手",
        page_icon="🎨",
        layout="wide"
    )
    
    st.title("🎨 AI图像生成提示词变奏创意助手")
    st.markdown("### 基于金字塔理论和MECE法则的完整提示词变奏系统")
    
    generator = PromptGenerator()
    
    with st.sidebar:
        st.header("📚 系统说明")
        st.markdown("""
        **金字塔结构（6大维度）：**
        1. **主体层** - 描述什么
        2. **风格层** - 如何表现  
        3. **环境层** - 在哪里
        4. **技术层** - 技术参数
        5. **氛围层** - 感觉如何
        6. **创新层** - 突破创新
        
        **MECE法则：**
        - **相互独立** - 各维度不重叠
        - **完全穷尽** - 涵盖所有可能
        """)
        
        st.divider()
        
        mode = st.radio(
            "选择工作模式：",
            ["📖 浏览金字塔结构", "✨ 生成随机提示词", "🔄 提示词变奏", "🔍 分析提示词", "📦 完整方案生成"]
        )
    
    if mode == "📖 浏览金字塔结构":
        show_pyramid_structure(generator)
    
    elif mode == "✨ 生成随机提示词":
        show_random_generation(generator)
    
    elif mode == "🔄 提示词变奏":
        show_variation_generation(generator)
    
    elif mode == "🔍 分析提示词":
        show_prompt_analysis(generator)
    
    else:  # 完整方案生成
        show_complete_solution(generator)


def show_pyramid_structure(generator):
    """显示金字塔结构浏览"""
    st.header("📖 金字塔结构浏览")
    
    dimensions = generator.get_all_dimensions()
    
    selected_dimension = st.selectbox(
        "选择要浏览的维度：",
        dimensions
    )
    
    if selected_dimension:
        dim_info = generator.get_dimension_info(selected_dimension)
        
        st.subheader(selected_dimension)
        st.info(f"**描述：** {dim_info.get('描述', '')}")
        
        subdimensions = generator.get_subdimensions(selected_dimension)
        
        tabs = st.tabs(subdimensions)
        
        for tab, subdim in zip(tabs, subdimensions):
            with tab:
                options = generator.get_options(selected_dimension, subdim)
                
                for category, elements in options.items():
                    st.markdown(f"**{category}**")
                    
                    cols = st.columns(4)
                    for idx, element in enumerate(elements):
                        with cols[idx % 4]:
                            st.button(
                                element, 
                                key=f"{selected_dimension}_{subdim}_{category}_{element}",
                                use_container_width=True
                            )
                    
                    st.divider()


def show_random_generation(generator):
    """显示随机生成功能"""
    st.header("✨ 随机提示词生成")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        dimensions_count = st.slider(
            "选择包含的维度数量：",
            min_value=1,
            max_value=6,
            value=4
        )
    
    with col2:
        include_quality = st.checkbox("包含质量词", value=True)
    
    if st.button("🎲 生成随机提示词", type="primary", use_container_width=True):
        result = generator.generate_random_prompt(
            include_quality=include_quality,
            dimensions_count=dimensions_count
        )
        
        st.success("✅ 生成成功！")
        
        st.subheader("📝 生成的提示词")
        st.code(result["提示词"], language=None)
        
        st.subheader("🔍 维度分解")
        for dim, element in result["维度分解"].items():
            st.markdown(f"- **{dim}**: {element}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 复制提示词"):
                st.toast("提示词已复制到剪贴板！")
        
        with col2:
            if st.button("🔄 再生成一次"):
                st.rerun()


def show_variation_generation(generator):
    """显示变奏生成功能"""
    st.header("🔄 提示词变奏生成")
    
    base_prompt = st.text_area(
        "输入基础提示词：",
        placeholder="例如：一位穿着汉服的少女，站在樱花树下",
        height=100
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        strategy = st.selectbox(
            "选择变奏策略：",
            list(VARIATION_STRATEGIES["变奏策略"].keys())
        )
    
    with col2:
        count = st.slider("生成变奏数量：", min_value=1, max_value=10, value=5)
    
    if strategy:
        strategy_info = VARIATION_STRATEGIES["变奏策略"][strategy]
        st.info(f"**策略说明：** {strategy_info['描述']}")
        
        with st.expander("查看策略方法"):
            for method in strategy_info["方法"]:
                st.markdown(f"- {method}")
    
    if st.button("🎨 生成变奏", type="primary", use_container_width=True):
        if not base_prompt:
            st.warning("请先输入基础提示词！")
        else:
            strategy_name = strategy.split(".")[1] if "." in strategy else strategy
            variations = generator.generate_variations(base_prompt, strategy_name, count)
            
            st.success(f"✅ 成功生成 {len(variations)} 个变奏！")
            
            for idx, var in enumerate(variations, 1):
                with st.expander(f"变奏 {idx}"):
                    st.markdown(f"**提示词：**")
                    st.code(var["变奏"], language=None)
                    
                    st.markdown("**变奏信息：**")
                    for key, value in var.items():
                        if key != "变奏":
                            st.markdown(f"- **{key}**: {value}")


def show_prompt_analysis(generator):
    """显示提示词分析功能"""
    st.header("🔍 提示词分析")
    
    prompt = st.text_area(
        "输入要分析的提示词：",
        placeholder="输入你的提示词，系统将分析其结构并给出建议",
        height=150
    )
    
    if st.button("🔬 分析提示词", type="primary", use_container_width=True):
        if not prompt:
            st.warning("请先输入提示词！")
        else:
            analysis = generator.analyze_prompt(prompt)
            
            st.success("✅ 分析完成！")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("覆盖维度数", len(analysis["覆盖维度"]))
            
            with col2:
                st.metric("建议补充数", len(analysis["建议补充"]))
            
            if analysis["识别的元素"]:
                st.subheader("✅ 已识别的元素")
                for dim, elements in analysis["识别的元素"].items():
                    with st.expander(dim):
                        for elem in elements:
                            st.markdown(f"- **{elem['子维度']}** / {elem['类别']}: `{elem['元素']}`")
            
            if analysis["建议补充"]:
                st.subheader("💡 建议补充的维度")
                for suggestion in analysis["建议补充"]:
                    with st.expander(suggestion["维度"]):
                        st.markdown(f"**说明：** {suggestion['描述']}")
                        st.markdown(f"**示例：** {suggestion['示例']}")
            else:
                st.success("🎉 恭喜！你的提示词已经覆盖了所有维度！")


def show_complete_solution(generator):
    """显示完整方案生成"""
    st.header("📦 完整提示词方案生成")
    
    st.markdown("""
    输入你的**核心创意**，系统将：
    1. 分析并丰富你的想法
    2. 生成完整的正向和负向提示词
    3. 提供6种策略的变奏方案
    4. 给出详细的统计信息
    """)
    
    base_idea = st.text_input(
        "输入核心创意：",
        placeholder="例如：赛博朋克风格的猫"
    )
    
    if st.button("🚀 生成完整方案", type="primary", use_container_width=True):
        if not base_idea:
            st.warning("请先输入核心创意！")
        else:
            with st.spinner("正在生成完整方案..."):
                result = generator.generate_complete_prompt_set(base_idea)
            
            st.success("✅ 完整方案生成成功！")
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 概览", "📝 提示词", "🔍 分析", "🎨 变奏方案", "📥 导出"
            ])
            
            with tab1:
                st.subheader("📊 方案统计")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("覆盖维度", result["统计"]["覆盖维度数"])
                with col2:
                    st.metric("补充建议", result["统计"]["建议补充数"])
                with col3:
                    st.metric("总变奏数", result["统计"]["总变奏数"])
                
                st.divider()
                
                st.markdown("**原始想法：**")
                st.info(result["原始想法"])
                
                st.markdown("**增强后：**")
                st.success(result["增强提示词"])
            
            with tab2:
                st.subheader("📝 完整提示词")
                
                st.markdown("**正向提示词：**")
                st.code(result["完整正向提示词"], language=None)
                
                st.markdown("**负向提示词：**")
                st.code(result["负向提示词"], language=None)
                
                if st.button("📋 复制正向提示词"):
                    st.toast("正向提示词已复制！")
                
                if st.button("📋 复制负向提示词"):
                    st.toast("负向提示词已复制！")
            
            with tab3:
                st.subheader("🔍 详细分析")
                
                analysis = result["分析结果"]
                
                if analysis["识别的元素"]:
                    st.markdown("**已包含的元素：**")
                    for dim, elements in analysis["识别的元素"].items():
                        with st.expander(dim):
                            for elem in elements:
                                st.markdown(f"- {elem['子维度']} / {elem['类别']}: `{elem['元素']}`")
                
                if analysis["建议补充"]:
                    st.markdown("**补充的元素：**")
                    for sugg in analysis["建议补充"]:
                        st.markdown(f"- **{sugg['维度']}**: {sugg['示例']}")
            
            with tab4:
                st.subheader("🎨 变奏方案")
                
                for strategy_name, variations in result["变奏方案"].items():
                    with st.expander(f"{strategy_name} ({len(variations)}个变奏)"):
                        for idx, var in enumerate(variations, 1):
                            st.markdown(f"**变奏 {idx}：**")
                            st.code(var["变奏"], language=None)
                            st.caption(f"策略：{var.get('策略', strategy_name)}")
                            st.divider()
            
            with tab5:
                st.subheader("📥 导出方案")
                
                export_format = st.radio(
                    "选择导出格式：",
                    ["JSON", "纯文本", "Markdown"]
                )
                
                if export_format == "JSON":
                    export_data = json.dumps(result, ensure_ascii=False, indent=2)
                    st.download_button(
                        "⬇️ 下载JSON文件",
                        data=export_data,
                        file_name="prompt_variations.json",
                        mime="application/json"
                    )
                
                elif export_format == "纯文本":
                    export_text = f"""AI图像生成提示词方案
========================

原始想法：{result['原始想法']}

完整正向提示词：
{result['完整正向提示词']}

负向提示词：
{result['负向提示词']}

变奏方案：
"""
                    for strategy_name, variations in result["变奏方案"].items():
                        export_text += f"\n{strategy_name}:\n"
                        for idx, var in enumerate(variations, 1):
                            export_text += f"  {idx}. {var['变奏']}\n"
                    
                    st.download_button(
                        "⬇️ 下载文本文件",
                        data=export_text,
                        file_name="prompt_variations.txt",
                        mime="text/plain"
                    )
                
                else:  # Markdown
                    export_md = f"""# AI图像生成提示词方案

## 原始想法
{result['原始想法']}

## 完整提示词

### 正向提示词
```
{result['完整正向提示词']}
```

### 负向提示词
```
{result['负向提示词']}
```

## 变奏方案
"""
                    for strategy_name, variations in result["变奏方案"].items():
                        export_md += f"\n### {strategy_name}\n\n"
                        for idx, var in enumerate(variations, 1):
                            export_md += f"{idx}. `{var['变奏']}`\n\n"
                    
                    st.download_button(
                        "⬇️ 下载Markdown文件",
                        data=export_md,
                        file_name="prompt_variations.md",
                        mime="text/markdown"
                    )


if __name__ == "__main__":
    main()
