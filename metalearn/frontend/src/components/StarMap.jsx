import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { useNavigate } from 'react-router-dom';

export default function StarMap({ topics, masteryScores = {} }) {
  const svgRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!svgRef.current || !topics?.length) return;

    const width = svgRef.current.clientWidth;
    const height = 700;
    const centerX = width / 2;
    const centerY = height / 2;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    svg.attr('viewBox', `0 0 ${width} ${height}`);

    const g = svg.append('g');

    const zoom = d3.zoom()
      .scaleExtent([0.3, 3])
      .on('zoom', (event) => g.attr('transform', event.transform));

    svg.call(zoom);
    svg.on('dblclick.zoom', null);

    const nodes = [];
    const links = [];

    topics.forEach((topic, ti) => {
      const angle = (2 * Math.PI * ti) / topics.length - Math.PI / 2;
      const radius = Math.min(width, height) * 0.28;
      const topicNode = {
        id: `topic-${topic.id}`,
        type: 'topic',
        label: topic.name,
        data: topic,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        mastery: masteryScores[topic.name] ?? 0,
        color: topic.color_hex || '#6366f1',
        category: topic.category,
      };
      nodes.push(topicNode);

      links.push({
        source: topicNode,
        target: { id: 'center', x: centerX, y: centerY },
        type: 'orbit',
      });

      (topic.learning_paths || []).forEach((path, pi) => {
        const pathAngle = angle + (pi - (topic.learning_paths.length - 1) / 2) * 0.35;
        const pathRadius = radius + 70;
        const pathNode = {
          id: `path-${path.id}`,
          type: 'path',
          label: path.name,
          data: path,
          topicId: topic.id,
          x: centerX + pathRadius * Math.cos(pathAngle),
          y: centerY + pathRadius * Math.sin(pathAngle),
          difficulty: path.difficulty_level,
          color: topic.color_hex || '#6366f1',
        };
        nodes.push(pathNode);

        links.push({
          source: topicNode,
          target: pathNode,
          type: 'path-link',
        });
      });
    });

    const centerNode = { id: 'center', type: 'center', label: 'MetaLearn', x: centerX, y: centerY };
    nodes.push(centerNode);

    const simulation = d3.forceSimulation(nodes)
      .force('center', d3.forceCenter(centerX, centerY).strength(0.05))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('link', d3.forceLink(links).id((d) => d.id).distance(120).strength(0.3))
      .force('collision', d3.forceCollide(40))
      .alphaDecay(0.02);

    const link = g.append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', (d) => d.type === 'orbit' ? 'rgba(99,102,241,0.15)' : 'rgba(255,255,255,0.08)')
      .attr('stroke-width', (d) => d.type === 'orbit' ? 1.5 : 1)
      .attr('stroke-dasharray', (d) => d.type === 'orbit' ? '4,4' : 'none');

    const node = g.append('g')
      .selectAll('g')
      .data(nodes)
      .join('g')
      .style('cursor', (d) => d.type !== 'center' ? 'pointer' : 'default')
      .call(d3.drag()
        .on('start', (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on('drag', (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on('end', (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        })
      );

    const defs = svg.append('defs');

    const gradients = {};
    topics.forEach((t) => {
      const id = `glow-${t.id}`;
      const color = t.color_hex || '#6366f1';
      const grad = defs.append('radialGradient').attr('id', id);
      grad.append('stop').attr('offset', '0%').attr('stop-color', color).attr('stop-opacity', 0.4);
      grad.append('stop').attr('offset', '100%').attr('stop-color', color).attr('stop-opacity', 0);
      gradients[t.id] = id;
    });
    defs.append('radialGradient').attr('id', 'center-glow')
      .append('stop').attr('offset', '0%').attr('stop-color', '#818cf8').attr('stop-opacity', 0.6);
    defs.select('#center-glow')
      .append('stop').attr('offset', '100%').attr('stop-color', '#818cf8').attr('stop-opacity', 0);

    node.each(function (d) {
      const el = d3.select(this);
      const r = d.type === 'center' ? 28 : d.type === 'topic' ? 22 + (d.mastery / 100) * 12 : 10;

      if (d.type === 'center') {
        el.append('circle').attr('r', 40).attr('fill', 'url(#center-glow)');
        el.append('circle').attr('r', 28).attr('fill', '#818cf8').attr('stroke', '#a5b4fc').attr('stroke-width', 2);
        el.append('text').attr('dy', 5).attr('text-anchor', 'middle').attr('fill', '#fff')
          .attr('font-size', 10).attr('font-weight', 'bold').text('ML');
      }

      if (d.type === 'topic') {
        el.append('circle')
          .attr('r', r + 12)
          .attr('fill', `url(#glow-${d.data.id})`);
        el.append('circle')
          .attr('r', r)
          .attr('fill', d3.color(d.color).darker(0.3))
          .attr('stroke', d.color)
          .attr('stroke-width', 2.5);
        el.append('circle')
          .attr('r', r * d.mastery / 100 || 2)
          .attr('fill', d.color)
          .attr('opacity', 0.6);
        el.append('text')
          .attr('dy', r + 16)
          .attr('text-anchor', 'middle')
          .attr('fill', '#c4b5fd')
          .attr('font-size', 11)
          .attr('font-weight', '600')
          .text(d.label);
      }

      if (d.type === 'path') {
        el.append('circle')
          .attr('r', r)
          .attr('fill', d3.color(d.color).darker(0.5))
          .attr('stroke', d.color)
          .attr('stroke-width', 1.5)
          .attr('opacity', 0.9);
        el.append('text')
          .attr('dy', r + 14)
          .attr('text-anchor', 'middle')
          .attr('fill', '#9ca3af')
          .attr('font-size', 8)
          .text(d.label.length > 15 ? d.label.slice(0, 15) + '...' : d.label);
      }
    });

    node.on('click', (event, d) => {
      event.stopPropagation();
      if (d.type === 'topic') {
        navigate(`/missions/${d.data.learning_paths?.[0]?.id || d.data.id}`);
      } else if (d.type === 'path') {
        navigate(`/missions/${d.data.id}`);
      }
    });

    node.on('mouseenter', function (event, d) {
      const el = d3.select(this);
      el.select('circle').transition().duration(200).attr('r', (c) => {
        const base = c?.__data__?.type === 'topic' ? 22 + (d.mastery / 100) * 12 + 4 : 14;
        return base;
      });
    });

    node.on('mouseleave', function () {
      d3.select(this).select('circle').transition().duration(200).attr('r', null);
    });

    const tooltip = d3.select('body').selectAll('.starmap-tooltip').data([0])
      .join('div')
      .attr('class', 'starmap-tooltip')
      .style('position', 'fixed')
      .style('display', 'none')
      .style('background', 'rgba(30,27,75,0.95)')
      .style('border', '1px solid rgba(99,102,241,0.5)')
      .style('border-radius', '12px')
      .style('padding', '12px 16px')
      .style('color', '#e2e8f0')
      .style('font-size', '13px')
      .style('pointer-events', 'none')
      .style('z-index', '1000')
      .style('backdrop-filter', 'blur(8px)')
      .style('min-width', '160px');

    node.on('mouseover', function (event, d) {
      if (d.type === 'center') {
        tooltip.style('display', 'none');
        return;
      }

      let html = `<strong style="color:${d.color}">${d.label}</strong>`;
      if (d.type === 'topic') {
        html += `<br><span style="color:#9ca3af;font-size:11px;">${d.category || ''}</span>`;
        html += `<br><span style="color:#818cf8;">Penguasaan: ${d.mastery}%</span>`;
        const pathCount = d.data.learning_paths?.length || 0;
        html += `<br><span style="color:#6b7280;font-size:11px;">${pathCount} jalur belajar</span>`;
      }
      if (d.type === 'path') {
        const badge = d.difficulty === 'beginner' ? '<span style="color:#4ade80;">Pemula</span>'
          : d.difficulty === 'intermediate' ? '<span style="color:#facc15;">Menengah</span>'
          : '<span style="color:#f87171;">Lanjutan</span>';
        html += `<br>${badge}`;
        const missionCount = d.data.missions?.length || 0;
        html += `<br><span style="color:#6b7280;font-size:11px;">${missionCount} misi</span>`;
      }
      html += '<br><span style="color:#6b7280;font-size:10px;">Klik untuk mulai</span>';

      tooltip.html(html)
        .style('display', 'block')
        .style('left', (event.clientX + 15) + 'px')
        .style('top', (event.clientY - 10) + 'px');
    });

    node.on('mousemove', function (event) {
      tooltip.style('left', (event.clientX + 15) + 'px').style('top', (event.clientY - 10) + 'px');
    });

    node.on('mouseout', function () {
      tooltip.style('display', 'none');
    });

    simulation.on('tick', () => {
      link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      node.attr('transform', (d) => `translate(${d.x},${d.y})`);
    });

    return () => {
      simulation.stop();
      tooltip.remove();
    };
  }, [topics, masteryScores, navigate]);

  return (
    <svg
      ref={svgRef}
      className="w-full h-full min-h-[500px]"
      style={{ background: 'transparent' }}
    />
  );
}
