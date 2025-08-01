import React, { useEffect, useRef, useState } from 'react';
import { Box, Typography } from '@mui/material';

interface CognitiveNode {
  id: string;
  name: string;
  description?: string;
  x: number;
  y: number;
}

interface CognitiveEdge {
  id: string;
  source: string;
  target: string;
  relationship_type: string;
  custom_name?: string;
}

interface CognitiveMapData {
  nodes: CognitiveNode[];
  edges: CognitiveEdge[];
}

interface SimpleCognitiveMapViewerProps {
  mapData?: CognitiveMapData | null;
}

const SimpleCognitiveMapViewer: React.FC<SimpleCognitiveMapViewerProps> = ({ mapData }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedEdgeId, setSelectedEdgeId] = useState<string | null>(null);

  useEffect(() => {
    if (!mapData || !svgRef.current) return;

    const svg = svgRef.current;
    const width = 480;
    const height = 400;

    // 清除之前的内容
    svg.innerHTML = '';

    // 设置SVG尺寸
    svg.setAttribute('width', width.toString());
    svg.setAttribute('height', height.toString());
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);

    // 创建箭头标记
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    marker.setAttribute('id', 'arrowhead');
    marker.setAttribute('viewBox', '0 -5 10 10');
    marker.setAttribute('refX', '15');
    marker.setAttribute('refY', '0');
    marker.setAttribute('markerWidth', '6');
    marker.setAttribute('markerHeight', '6');
    marker.setAttribute('orient', 'auto');

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M0,-5L10,0L0,5');
    path.setAttribute('fill', '#666');

    marker.appendChild(path);
    defs.appendChild(marker);
    svg.appendChild(defs);

    // 计算节点位置（简单的圆形布局）
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 3;

    const positionedNodes = mapData.nodes.map((node, index) => {
      const angle = (index / mapData.nodes.length) * 2 * Math.PI;
      return {
        ...node,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle)
      };
    });

    // 绘制连线
    mapData.edges.forEach((edge, index) => {
      const sourceNode = positionedNodes.find(n => n.id === edge.source);
      const targetNode = positionedNodes.find(n => n.id === edge.target);

      if (sourceNode && targetNode) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', sourceNode.x.toString());
        line.setAttribute('y1', sourceNode.y.toString());
        line.setAttribute('x2', targetNode.x.toString());
        line.setAttribute('y2', targetNode.y.toString());
        line.setAttribute('stroke', selectedEdgeId === edge.id ? '#ff4444' : '#999');
        line.setAttribute('stroke-width', selectedEdgeId === edge.id ? '3' : '2');
        line.setAttribute('marker-end', 'url(#arrowhead)');
        line.style.cursor = 'pointer';

        line.addEventListener('click', () => {
          setSelectedEdgeId(edge.id === selectedEdgeId ? null : edge.id);
        });

        line.addEventListener('mouseover', () => {
          if (edge.id !== selectedEdgeId) {
            line.setAttribute('stroke', '#ff4444');
            line.setAttribute('stroke-width', '3');
          }
        });

        line.addEventListener('mouseout', () => {
          if (edge.id !== selectedEdgeId) {
            line.setAttribute('stroke', '#999');
            line.setAttribute('stroke-width', '2');
          }
        });

        svg.appendChild(line);

        // 添加连线标签
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', ((sourceNode.x + targetNode.x) / 2).toString());
        text.setAttribute('y', ((sourceNode.y + targetNode.y) / 2 - 5).toString());
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('font-size', '10px');
        text.setAttribute('fill', '#333');
        text.textContent = edge.custom_name || edge.relationship_type;

        svg.appendChild(text);
      }
    });

    // 绘制节点
    positionedNodes.forEach((node, index) => {
      const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      group.style.cursor = 'pointer';

      // 节点圆圈
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', node.x.toString());
      circle.setAttribute('cy', node.y.toString());
      circle.setAttribute('r', '25');
      circle.setAttribute('fill', getNodeColor(node.name));
      circle.setAttribute('stroke', '#333');
      circle.setAttribute('stroke-width', '2');

      circle.addEventListener('mouseover', () => {
        circle.setAttribute('r', '30');
      });

      circle.addEventListener('mouseout', () => {
        circle.setAttribute('r', '25');
      });

      group.appendChild(circle);

      // 节点文本
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', node.x.toString());
      text.setAttribute('y', node.y.toString());
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('dy', '0.35em');
      text.setAttribute('font-size', '10px');
      text.setAttribute('fill', 'white');
      text.setAttribute('font-weight', 'bold');
      
      const maxLength = 8;
      const displayText = node.name.length > maxLength ? 
        node.name.substring(0, maxLength) + "..." : node.name;
      text.textContent = displayText;

      group.appendChild(text);

      // 添加标题
      const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
      title.textContent = `${node.name}${node.description ? `\n${node.description}` : ''}`;
      group.appendChild(title);

      svg.appendChild(group);
    });

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
      <svg 
        ref={svgRef} 
        style={{ 
          width: '100%', 
          height: '100%', 
          border: '1px solid #e0e0e0', 
          borderRadius: '4px',
          backgroundColor: '#fafafa'
        }} 
      />
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
      <Box 
        sx={{ 
          position: 'absolute', 
          bottom: 10, 
          left: 10, 
          bgcolor: 'rgba(0,0,0,0.7)', 
          color: 'white', 
          px: 1, 
          py: 0.5, 
          borderRadius: 1,
          fontSize: '10px'
        }}
      >
        💡 点击连线选择 | 悬停查看详情
      </Box>
    </Box>
  );
};

export default SimpleCognitiveMapViewer;
