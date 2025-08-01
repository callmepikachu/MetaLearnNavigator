import React, { useEffect, useRef, useState } from 'react';
import { Box, Typography, CircularProgress } from '@mui/material';
import * as d3 from 'd3';

interface CognitiveNode extends d3.SimulationNodeDatum {
  id: string;
  name: string;
  description?: string;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
}

interface CognitiveEdge extends d3.SimulationLinkDatum<CognitiveNode> {
  id: string;
  source: string | CognitiveNode;
  target: string | CognitiveNode;
  relationship_type: string;
  custom_name?: string;
}

interface CognitiveMapData {
  nodes: CognitiveNode[];
  edges: CognitiveEdge[];
}

interface CognitiveMapViewerProps {
  mapData?: CognitiveMapData | null;
}

const CognitiveMapViewer: React.FC<CognitiveMapViewerProps> = ({ mapData }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedEdgeId, setSelectedEdgeId] = useState<string | null>(null);

  useEffect(() => {
    if (!mapData || !svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove(); // 清除之前的内容

    const width = 480;
    const height = 400;

    svg.attr("width", width).attr("height", height);

    // 创建箭头标记
    const defs = svg.append("defs");

    defs.append("marker")
      .attr("id", "arrowhead")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 15)
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", "#666");

    // 创建力导向布局
    const simulation = d3.forceSimulation<CognitiveNode>(mapData.nodes)
      .force("link", d3.forceLink<CognitiveNode, CognitiveEdge>(mapData.edges).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(30));

    // 绘制连线
    const links = svg.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(mapData.edges)
      .enter()
      .append("line")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .attr("stroke-width", 2)
      .attr("marker-end", "url(#arrowhead)")
      .style("cursor", "pointer")
      .on("click", (event, d) => {
        setSelectedEdgeId(d.id === selectedEdgeId ? null : d.id);
        console.log("Edge clicked:", d);
      })
      .on("mouseover", function(event, d) {
        d3.select(this).attr("stroke", "#ff4444").attr("stroke-width", 3);
      })
      .on("mouseout", function(event, d) {
        if (d.id !== selectedEdgeId) {
          d3.select(this).attr("stroke", "#999").attr("stroke-width", 2);
        }
      });

    // 添加连线标签
    const linkLabels = svg.append("g")
      .attr("class", "link-labels")
      .selectAll("text")
      .data(mapData.edges)
      .enter()
      .append("text")
      .attr("text-anchor", "middle")
      .attr("font-size", "10px")
      .attr("fill", "#333")
      .attr("dy", -5)
      .text(d => d.custom_name || d.relationship_type);

    // 绘制节点
    const nodes = svg.append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(mapData.nodes)
      .enter()
      .append("g")
      .attr("class", "node")
      .style("cursor", "pointer")
      .call(d3.drag<SVGGElement, CognitiveNode>()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    // 节点圆圈
    nodes.append("circle")
      .attr("r", 25)
      .attr("fill", d => getNodeColor(d.name))
      .attr("stroke", "#333")
      .attr("stroke-width", 2)
      .on("mouseover", function(event, d) {
        d3.select(this).attr("r", 30);
      })
      .on("mouseout", function(event, d) {
        d3.select(this).attr("r", 25);
      });

    // 节点文本
    nodes.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "0.35em")
      .attr("font-size", "10px")
      .attr("fill", "white")
      .attr("font-weight", "bold")
      .text(d => {
        const maxLength = 8;
        return d.name.length > maxLength ? d.name.substring(0, maxLength) + "..." : d.name;
      });

    // 节点标题（悬停显示完整信息）
    nodes.append("title")
      .text(d => `${d.name}${d.description ? `\n${d.description}` : ""}`);

    // 更新位置的函数
    function ticked() {
      links
        .attr("x1", (d: CognitiveEdge) => (d.source as CognitiveNode).x || 0)
        .attr("y1", (d: CognitiveEdge) => (d.source as CognitiveNode).y || 0)
        .attr("x2", (d: CognitiveEdge) => (d.target as CognitiveNode).x || 0)
        .attr("y2", (d: CognitiveEdge) => (d.target as CognitiveNode).y || 0);

      linkLabels
        .attr("x", (d: CognitiveEdge) => ((d.source as CognitiveNode).x! + (d.target as CognitiveNode).x!) / 2)
        .attr("y", (d: CognitiveEdge) => ((d.source as CognitiveNode).y! + (d.target as CognitiveNode).y!) / 2);

      nodes
        .attr("transform", (d: CognitiveNode) => `translate(${d.x || 0},${d.y || 0})`);
    }

    // 拖拽函数
    function dragstarted(event: d3.D3DragEvent<SVGGElement, CognitiveNode, CognitiveNode>, d: CognitiveNode) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: d3.D3DragEvent<SVGGElement, CognitiveNode, CognitiveNode>, d: CognitiveNode) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event: d3.D3DragEvent<SVGGElement, CognitiveNode, CognitiveNode>, d: CognitiveNode) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // 启动模拟
    simulation.on("tick", ticked);

    // 清理函数
    return () => {
      simulation.stop();
    };

  }, [mapData, selectedEdgeId]);

  // 根据节点名称生成颜色
  const getNodeColor = (name: string): string => {
    const colors = [
      "#4CAF50", "#2196F3", "#FF9800", "#9C27B0",
      "#F44336", "#00BCD4", "#795548", "#607D8B"
    ];
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
  };

  if (!mapData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100%" flexDirection="column">
        <Typography variant="body1" color="text.secondary">
          暂无认知地图
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          请先输入学习问题并进行任务拆解
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', height: '100%', overflow: 'hidden', position: 'relative' }}>
      <svg ref={svgRef} style={{ width: '100%', height: '100%', border: '1px solid #e0e0e0', borderRadius: '4px' }} />
      {selectedEdgeId && (
        <Box
          sx={{
            position: 'absolute',
            top: 10,
            right: 10,
            bgcolor: 'primary.main',
            color: 'white',
            px: 1,
            py: 0.5,
            borderRadius: 1,
            fontSize: '12px'
          }}
        >
          已选择连线: {selectedEdgeId}
        </Box>
      )}
    </Box>
  );
};

export default CognitiveMapViewer;
