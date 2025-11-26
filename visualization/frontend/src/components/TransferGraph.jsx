import React, { useEffect, useRef } from "react";
import { Graph, NodeEvent, EdgeEvent, CanvasEvent, Minimap } from '@antv/g6';

export default function TransferGraph() {
  const ref = useRef();

  useEffect(() => {
    // 获取数据并渲染图
    fetch('/api/graph/init')
      .then(res => res.json())
      .then(data => {
        // 如果已有图实例，先销毁
        if (ref.current && ref.current.graph) {
          ref.current.graph.destroy();
        }
       

        // 创建Graph实例
        const graph = new Graph({
          container: ref.current,
          data,
          node: {
            style: {
              labelText: d => d.label,
              labelPlacement: 'middle',
              labelFill: '#fff',
            },
            palette: {
              type: 'group',
              field: d => d.combo,
            },
          },
          combo: {
            style: {
              labelText: d => d.data?.label || d.id,
              fill: '#f0f0f0',
              stroke: '#ccc',
              lineWidth: 1,
            },
          },
          edge: {
            style: {
              stroke: '#99ADD1',
              lineWidth: 1,
              endArrow: true,  // 增加方向性箭头
            },
          },
          layout: {
            type: 'combo-combined',
            comboPadding: 50,  // 设置combo之间的间距
            nodeSpacing: 30,   // 设置节点之间的间距
            preventOverlap: true,
          },
          behaviors: [
            {
              type: 'drag-element',
              dropEffect: 'link',
            },  // 改为drag-element，恢复拖拽功能
            'drag-canvas', 'zoom-canvas','collapse-expand',
          ],
          autoFit: 'view',
          plugins: [
            {
              type: 'contextmenu',
              trigger: 'contextmenu',
              getItems: (e) => {
                if (e.target.id) {
                  return [
                    {
                      name: '删除节点',
                      value: 'delete',
                    },
                  ];
                }
                if (e.target.type === 'edge') {
                  return [
                    {
                      name: '移动边',
                      value: 'move',
                    },
                  ];
                }
                return [];
              },
            },
          ],
        });
        // 获取所有插件配置
const plugins = graph.getPlugins();

// 查看当前激活的插件
console.log('当前图表的插件配置:', plugins);
        // graph.setPlugins([
        //   // 字符串形式（使用默认配置）
        //   'minimap',
        
        //   // 对象形式（自定义配置）
        //   {
        //     type: 'grid',
        //     key: 'grid-line',
        //   },
        //   {
        //     type: 'toolbar',
        //     key: 'graph-toolbar',
        //     position: 'top-right',
        //   },
        // ]);
        graph.on(CanvasEvent.DBLCLICK, async (evt) => {
          await graph.layout();
        });

        // 监听节点点击事件
        graph.on(NodeEvent.CLICK, async (evt) => {
          const { target } = evt;
          console.log(`节点 ${target.id} 被点击了`);
          const nodeData = graph.getNodeData(target.id);
          console.log('节点数据:', nodeData);
          graph.setElementState(target.id, 'selected');

          try {
            const res = await fetch(`/api/address/${target.id}/top-tx`);
            const newData = await res.json();
            console.log('获取到的新数据:', newData);
            
            // 1. 先创建新节点
            console.log('开始创建新节点...');
            graph.addData(newData);
            console.log('所有节点创建完成',newData);
            await graph.draw(); // 刷新画布显示新节点
            await graph.layout();
            

          } catch (e) {
            console.error("获取数据失败", e);
          }
        });

        // // 监听边的鼠标进入事件
        // graph.on(EdgeEvent.POINTER_OVER, (evt) => {
        //   const { target } = evt;
        //   graph.setElementState(target.id, 'highlight');
        // });

        // // 监听画布拖拽事件
        // graph.on(CanvasEvent.DRAG, (evt) => {
        //   console.log('画布正在被拖拽');
        // });

        graph.render();
        // 保存graph实例，便于后续销毁
        ref.current.graph = graph;
      });
    // 卸载时销毁graph
    return () => {
      if (ref.current && ref.current.graph) {
        ref.current.graph.destroy();
      }
    };
  }, []);

  return (
    <div>
      {/* 图容器 */}
      <div id="container" ref={ref} style={{ width: 900, height: 600 }} />
    </div>
  );
} 