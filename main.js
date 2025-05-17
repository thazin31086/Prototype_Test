import * as d3 from 'd3';
import data from './cyber_incident_output.json' assert { type: 'json' };

const margin = { top: 30, right: 0, bottom: 30, left: 40 },
      width = 450 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

const svg = d3.select("body")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Get unique days and hours
const days = Array.from(new Set(data.map(d => d.day)));
const hours = Array.from(new Set(data.map(d => d.hour)));

// Scales
const x = d3.scaleBand().range([0, width]).domain(hours).padding(0.05);
const y = d3.scaleBand().range([height, 0]).domain(days).padding(0.05);
const color = d3.scaleSequential(d3.interpolateInferno)
  .domain([0, d3.max(data, d => d.value)]);

// Axes
svg.append("g")
   .call(d3.axisTop(x).tickFormat(d => `${d}:00`));
svg.append("g")
   .call(d3.axisLeft(y));

// Heatmap squares
svg.selectAll()
  .data(data, d => d.day + ':' + d.hour)
  .join("rect")
    .attr("x", d => x(d.hour))
    .attr("y", d => y(d.day))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .style("fill", d => color(d.value))
    .style("stroke", "#000");
