// panel class definition
var EpisecChartPanel = function(options) {
	
	var widgetid = options.widgetid;
    var data = options.data,dates = options.dates;
	var chartBody, gPanel, signalBody;
	var svg = options.svg;
    var ymax,ymin,yScale,yAxis,gY,cgY,movingytick,movingytickrect,movingyticktext;
	var gCandles, gVolumes, gBars, gBricks, gLineBreaks, gKagis, gShapes, gSignals;
	var gRect;
	var candles, stems, volumes, yband, bars, bricks, linebreaks, kagis;
	var asset = options.asset;

	var dateFormat = options.dateFormat;
	
	var gInfoBars = new Map();
	var closebuttons = new Map();
	var infovalues = new Map();
	
	var gIndicators = new Map();
	var indicators = new Map();			// indicatorid:plotname:data

	var indicators_info = new Map(); 	// indicatorid:{id,name,data}


	for(var i=0; i<options.indicators_info.length; i++)	{
		indicators_info.set(options.indicators_info[i].id, {
			id : options.indicators_info[i].id,
			name : options.indicators_info[i].name,
			data : options.indicators_info[i].data,
			tii_id : options.indicators_info[i].tii_id
		});
	}


    var chartType = options.chartType;	
	var panelType = options.panelType;	// main panel or indicator panel
	
	var x = options.x;
	var y = options.y;
    var w = options.width;
	var h = options.height;
	
	var xRescale = options.xRescale,tk = options.tk;
	var xDateScale = options.xDateScale;
	var xBand = options.xBand;
	var xBandv = options.xBandv;
	var xBandnp = options.xBandnp;
	var infoids = [];

	var trade_id = options.trade_id;
	
	var removePanelCallback = options.removePanelCallback;
	var removeIndicatorCallback = options.removeIndicatorCallback;
	var focusPanelCallback = options.focusPanelCallback;
	var settingViewCallback = options.settingViewCallback;
	var requireAddIndicatorCallback = options.requireAddIndicatorCallback;

	var indsettings = new Map();
    
    function createShapeBody(){
		gShapes = chartBody.append("g")
						.attr("class", "shapes");
	}

	function createSignalBody(){
		gSignals = chartBody.append("g")
						.attr("class", "signals");
	}
	
	function removeShapeBody(){
		gShapes.remove();
	}

	function removeSignalBody(){
		gSignals.remove();
	}

	this.removeAllShapes = function() {
		gShapes.selectAll(".shape")
			.remove();
	};

	this.removeAllSignals = function() {
		gSignals.selectAll(".signal")
			.remove();
	};

	function makeEllipsePoints(points) {		//////////////////////// calculate ?????????????
		var centerindex = (points[1].index + points[0].index) / 2;
		var centerprice = (points[1].price + points[0].price) / 2;
		var rx = Math.abs(points[2].index - points[0].index);
		var ry = Math.abs(points[2].price - points[0].price);
		return {cx:centerindex, cy:centerprice, rx:rx, ry:ry};
	}

	function makeRectanglePoints(points) {		//////////////////////// calculate ?????????????
		return {x:Math.min(points[0].index,points[1].index), y:Math.max(points[0].price,points[1].price), width:Math.abs(points[1].index - points[0].index), height:Math.abs(points[1].price - points[0].price)};

	}

	this.createSignalShape = function(data){

		if(data.type == 'signal-line'){
			gSignals.append('line')
				.data(data)
				.attr('class', data.name)
				.attr('x1', d => xRescale(d.x1))
				.attr('y1', d => yScale(d.y1))
				.attr('x2', d => xRescale(d.x2))
				.attr('y2', d => yScale(d.y2))
		}
		else if(data.type == 'signal-ovbs'){
			gSignals.selectAll('.signal-ovbs')
				.data(data.data)
				.enter()
				.append('line')
				.attr('class', 'signal-ovbs')
				.attr('x1', d => xRescale(d.x))
				.attr('y1', d => yScale(d.y)-50)
				.attr('x2', d => xRescale(d.x))
				.attr('y2', d => yScale(d.y)-10)
				.attr("marker-end", "url(#triangle_red)")
		}
		else if(data.type == 'signal-ovbe'){
			gSignals.selectAll('.signal-ovbe')
				.data(data.data)
				.enter()
				.append('line')
				.attr('class', 'signal-ovbe')
				.attr('x1', d => xRescale(d.x))
				.attr('y1', d => yScale(d.y)-50)
				.attr('x2', d => xRescale(d.x))
				.attr('y2', d => yScale(d.y)-10)
				.attr("marker-end", "url(#triangle_green)")
		}
		else if(data.type == 'signal-ovss'){
			gSignals.selectAll('.signal-ovss')
				.data(data.data)
				.enter()
				.append('line')
				.attr('class', 'signal-ovss')
				.attr('x1', d => xRescale(d.x))
				.attr('y1', d => yScale(d.y)+50)
				.attr('x2', d => xRescale(d.x))
				.attr('y2', d => yScale(d.y)+10)
				.attr("marker-end", "url(#triangle_red)")
		}
		else if(data.type == 'signal-ovse'){
			gSignals.selectAll('.signal-ovse')
				.data(data.data)
				.enter()
				.append('line')
				.attr('class', 'signal-ovse')
				.attr('x1', d => xRescale(d.x))
				.attr('y1', d => yScale(d.y)+50)
				.attr('x2', d => xRescale(d.x))
				.attr('y2', d => yScale(d.y)+10)
				.attr("marker-end", "url(#triangle_green)")
		}
		else if(data.type == 'signal-threshold-ovb'){
			gSignals.selectAll('.signal-threshold-ovb')
				.data(data.y)
				.enter()
				.append('line')
				.attr('class', 'signal-threshold-ovb')
				.attr('x1', xRescale(0))
				.attr('y1', d => yScale(d))
				.attr('x2', xRescale(dates.length))
				.attr('y2', d => yScale(d))
		}
		else if(data.type == 'signal-threshold-ovs'){
			gSignals.selectAll('.signal-threshold-ovs')
				.data(data.y)
				.enter()
				.append('line')
				.attr('class', 'signal-threshold-ovs')
				.attr('x1', xRescale(0))
				.attr('y1', d => yScale(d))
				.attr('x2', xRescale(dates.length))
				.attr('y2', d => yScale(d))
		}
	}

	this.createMultipointShape = function(points, options){
		switch(options.shape) {
			case 'ellipse':
				var pt = makeEllipsePoints(points);
				gShapes.append('ellipse')
					.data([pt])
					.attr('class', 'shape')
					.attr('cx', d => xRescale(d.cx))
					.attr('cy', d => yScale(d.cy))
					.attr('rx', d => xRescale(d.cx+d.rx) - xRescale(d.cx))
					.attr('ry', d => yScale(d.cy) - yScale(d.cy+d.ry))
				break;
			case 'rectangle':
				var pt = makeRectanglePoints(points);
				gShapes.append('rect')
					.data([pt])
					.attr('class', 'shape')
					.attr('x', d => xRescale(d.x))
					.attr('y', d => yScale(d.y))
					.attr('width', d => xRescale(d.x+d.width) - xRescale(d.x))
					.attr('height', d => yScale(d.y) - yScale(d.y+d.height))

				break;
			default:
				break;
		}
	};

	function drawShapes(){

		gShapes.selectAll('ellipse')
			.attr('cx', d => xRescale(d.cx))
			.attr('cy', d => yScale(d.cy))
			.attr('rx', d => xRescale(d.cx+d.rx) - xRescale(d.cx))
			.attr('ry', d => yScale(d.cy) - yScale(d.cy+d.ry))

		gShapes.selectAll('rect')
			.attr('x', d => xRescale(d.x))
			.attr('y', d => yScale(d.y))
			.attr('width', d => xRescale(d.x+d.width) - xRescale(d.x))
			.attr('height', d => yScale(d.y) - yScale(d.y+d.height))

	}

	function drawSignals(){


		// gSignals.selectAll('line')
		// 	.attr('x1', d => xRescale(d.x1))
		// 	.attr('y1', d => yScale(d.y1))
		// 	.attr('x2', d => xRescale(d.x2))
		// 	.attr('y2', d => yScale(d.y2))

		gSignals.selectAll('.signal-ovbs')
			.attr('x1', d => xRescale(d.x))
			.attr('y1', d => yScale(d.y)-50)
			.attr('x2', d => xRescale(d.x))
			.attr('y2', d => yScale(d.y)-10)

		gSignals.selectAll('.signal-ovbe')
			.attr('x1', d => xRescale(d.x))
			.attr('y1', d => yScale(d.y)-50)
			.attr('x2', d => xRescale(d.x))
			.attr('y2', d => yScale(d.y)-10)

		gSignals.selectAll('.signal-ovss')
			.attr('x1', d => xRescale(d.x))
			.attr('y1', d => yScale(d.y)+50)
			.attr('x2', d => xRescale(d.x))
			.attr('y2', d => yScale(d.y)+10)
		
		gSignals.selectAll('.signal-ovse')
			.attr('x1', d => xRescale(d.x))
			.attr('y1', d => yScale(d.y)+50)
			.attr('x2', d => xRescale(d.x))
			.attr('y2', d => yScale(d.y)+10)

		gSignals.selectAll('.signal-threshold-ovb')
			.attr('x1', xRescale(0))
			.attr('y1', d => yScale(d))
			.attr('x2', xRescale(dates.length))
			.attr('y2', d => yScale(d))

		gSignals.selectAll('.signal-threshold-ovs')
			.attr('x1', xRescale(0))
			.attr('y1', d => yScale(d))
			.attr('x2', xRescale(dates.length))
			.attr('y2', d => yScale(d))
	}

	function createCandles() {
		////////////// draw candlestick
		
		// draw rectangles
		gCandles = chartBody.append("g")
						.attr("class", "candles");

		candles = gCandles.selectAll(".candle")
		   .data(data)
		   .enter()
		   .append("rect")
		   .attr("class", d => (d.Open >= d.Close) ? "candle bearish" : "candle bullish")

		// create high and low
		stems = gCandles.selectAll("g.line")
		   .data(data)
		   .enter()
		   .append("line")
		   .attr("class", d => (d.Open >= d.Close) ? "stem bearish" : "stem bullish")
	}

	function removeCandles() {
		gCandles.remove()
	}

	function drawCandles() {
		
		candles.attr('x', (d, i) => xRescale(i) - xBand.bandwidth()*tk/2)
			.attr('y', d => yScale(Math.max(d.Open, d.Close)))
			.attr('width', xBand.bandwidth()*tk)
			.attr('height', d => (d.Open === d.Close) ? 1 : yScale(Math.min(d.Open, d.Close))-yScale(Math.max(d.Open, d.Close)))

		// draw high and low
		stems.attr("x1", (d, i) => xRescale(i))
		   .attr("x2", (d, i) => xRescale(i))
		   .attr("y1", d => yScale(d.High))
		   .attr("y2", d => yScale(d.Low))
	}

	function createBand() { //for the mouse moving event capture
		//make bands price
		gYband = gPanel.append("g")
			.attr("class", "yband");
  
		yband = gYband.append("line")
			.attr("class", "yband")
			.attr("x1", 0)
			.attr("y1", 0)
			.attr("y2", 0)
			.attr("x2", w)
	}

	function createBars() {
		// draw bars
		gBars = chartBody.append("g")
					.attr("class", "bars");

		bars = gBars.selectAll(".bar")
		   .data(data)
		   .enter()
		   .append("path")
		   .attr("class", d => (d.Open >= d.Close) ? "bar bearish" : "bar bullish");

		// create high and low
		stems = gBars.selectAll("g.line")
		   .data(data)
		   .enter()
		   .append("line")
		   .attr("class", d => (d.Open >= d.Close) ? "stem bearish" : "stem bullish")
	}

	function removeBars() {
		gBars.remove();
	}

	function drawBars() {
		bars.attr('d', (d, i) => "M" + (xRescale(i) - xBand.bandwidth()*tk/2) + " " + yScale(d.Open) + " H " + xRescale(i) + " V " + yScale(d.Close) + " H " + (xRescale(i)+xBand.bandwidth()*tk/2))

		// draw high and low
		stems.attr("x1", (d, i) => xRescale(i))
		   .attr("x2", (d, i) => xRescale(i))
		   .attr("y1", d => yScale(d.High))
		   .attr("y2", d => yScale(d.Low))
	}

	function createRenkos() {
		// draw rectangles
		gBricks = chartBody.append("g")
						.attr("class", "bricks");

		bricks = gBricks.selectAll(".brick")
		   .data(data)
		   .enter()
           .append("rect")
           .attr("class", d => "brick " + d.Trending)
	}

	function removeRenkos() {
		gBricks.remove()
	}

	function drawRenkos() {
		bricks.attr('x', (d, i) => xRescale(i) - xBandnp.bandwidth()*tk/2)
           .attr('width', xBandnp.bandwidth()*tk)
		   .attr('y', d => yScale(d.High))
		   .attr('height', d => yScale(d.Low) - yScale(d.High))
	}

	function createLinebreaks() {
		gLineBreaks = chartBody.append("g")
						.attr("class", "linebreaks");

		linebreaks = gLineBreaks.selectAll(".linebreak")
		   .data(data)
		   .enter()
           .append("rect")
           .attr("class", d => "linebreak " + d.Trending)
	}

	function removeLinebreaks() {
		gLineBreaks.remove()
	}

	function drawLinebreaks() {
		
		linebreaks.attr('x', (d, i) => xRescale(i) - xBand.bandwidth()*tk/2)
           .attr('width', xBand.bandwidth()*tk)
		   .attr('y', d => yScale(d.High))
		   .attr('height', d => yScale(d.Low) - yScale(d.High))
	}

	function createKagis() {
		gKagis = chartBody.append("g")
						.attr("class", "kagis");
						
		kagis = gKagis.selectAll(".kagi")
			.data(data)
			.enter()
        	.append("line")
        	.attr("class", d => "kagi " + d.Trending)
	}

	function removeKagis() {
		gKagis.remove()
	}

	function drawKagis() {

		kagis.attr("x1", d => d.Type == 'v' ? xRescale(d.x) : xRescale(d.x1))
			.attr("x2", d => d.Type == 'v' ? xRescale(d.x) : xRescale(d.x2))
			.attr("y1", d => yScale(d.fromClose))
			.attr("y2", d => yScale(d.toClose))
			.attr("stroke-width", 2*tk)
	}

	function createVolumes(){
		// draw volume bars
		gVolumes = chartBody.append("g")
					.attr("class", "volumes");

		volumes = gVolumes.selectAll(".volume")
		   .data(data)
		   .enter()
		   .append("rect")
		   .attr("class", d => (d.Open >= d.Close) ? "volume bearish" : "volume bullish")
	}

	function removeVolumes() {
		gVolumes.remove()
	}

	function drawVolumes(){
		// draw volume bars
		var vMaxheight = h*0.25;
		var vMax = d3.max(data.map(r => r.Volume));

		volumes.attr("x", (d, i) => xRescale(i) - xBandv.bandwidth()*tk/2)
		   .attr("y", d => h - d.Volume / vMax * vMaxheight)
		   .attr("width", xBandv.bandwidth()*tk)
		   .attr("height", d => d.Volume / vMax * vMaxheight)
	}

	function createChartBody(){
		chartBody = gPanel.append("g")
						.attr("class", "chartBody")
						.attr("clip-path", "url(#clip" + widgetid + "_" + trade_id + ")");
                        
        if(panelType == EPISEC_MAIN_PANEL) {
            if(chartType == EPISEC_CANDLESTICK || chartType == EPISEC_HEIKINASHI) {
                createCandles();
                createVolumes();
            }
            else if(chartType == EPISEC_BAR) {
                createBars();
                createVolumes();
            }
            else if(chartType == EPISEC_LINEBREAK) {
                createLinebreaks();
            }
            else if(chartType == EPISEC_RENKO) {
                createRenkos();
            }
            else if(chartType == EPISEC_KAGI) {
                createKagis();
			}
		}
		createIndicators();

	}

	function drawChartBody(){
        if(panelType == EPISEC_MAIN_PANEL) {
            if(chartType == EPISEC_CANDLESTICK || chartType == EPISEC_HEIKINASHI) {
                drawCandles();
                drawVolumes();
            }
            else if(chartType == EPISEC_BAR) {
                drawBars();
                drawVolumes();
            }
            else if(chartType == EPISEC_LINEBREAK) {
                drawLinebreaks();
            }
            else if(chartType == EPISEC_RENKO) {
                drawRenkos();
            }
            else if(chartType == EPISEC_KAGI) {
                drawKagis();
            }
		}
		
		drawIndicators();

		gPanel.selectAll(".closebutton").raise();
	}

	function removeChartBody(){
		if(chartType == EPISEC_CANDLESTICK || chartType == EPISEC_HEIKINASHI) {
			removeCandles();
			removeVolumes();
		}
		else if(chartType == EPISEC_BAR) {
			removeBars();
			removeVolumes();
		}
		else if(chartType == EPISEC_LINEBREAK) {
			removeLinebreaks();
		}
		else if(chartType == EPISEC_RENKO) {
			removeRenkos();
		}
		else if(chartType == EPISEC_KAGI) {
			removeKagis();
		}
    }
    
    function prepareScale() {
        if(panelType == EPISEC_MAIN_PANEL) {
            if(chartType == EPISEC_CANDLESTICK || chartType == EPISEC_BAR || chartType == EPISEC_HEIKINASHI || chartType == EPISEC_LINEBREAK || chartType == EPISEC_RENKO){
                ymax = d3.max(data.map(r => r.High));
                ymin = d3.min(data.map(r => r.Low));
            }
            else if(chartType == EPISEC_KAGI){
                ymax = d3.max(data, function(d) { return Math.max(d.fromClose, d.toClose); });
                ymin = d3.min(data, function(d) { return Math.min(d.fromClose, d.toClose); });
            }
        }
        else if(panelType == EPISEC_INDICATOR_PANEL) {
			ymax = 0;
			ymin = 1000000000;
			indicators_info.forEach( function( v, k, m ) {
				var nymax = d3.max(v.data, function(d) { return d3.max(d.y); });
				var nymin = d3.min(v.data, function(d) { return d3.min(d.y); });
				ymax = Math.max(nymax, ymax);
				ymin = Math.min(nymin, ymin);
			});
            
        }
        
		yScale = d3.scaleLinear().domain([ymin, ymax]).range([h, 0]).nice();
		prepareRescale();
	}
	
	function prepareRescale() {
		if(panelType == EPISEC_MAIN_PANEL) {
            //change price series
            if(chartType == EPISEC_KAGI) {
                var filtered = _.filter(data, d => ((d.x1 >= xRescale.domain()[0]) && (d.x2 <= xRescale.domain()[1])))
                    minP = +d3.min(filtered, function(d) { return Math.min(d.fromClose, d.toClose); })
                    maxP = +d3.max(filtered, function(d) { return Math.max(d.fromClose, d.toClose); })
                    buffer = (maxP - minP) * 0.1

                yScale.domain([minP - buffer, maxP + buffer])
            }
            else {
                var xmin = new Date(xDateScale(Math.floor(xRescale.domain()[0])))
                    xmax = new Date(xDateScale(Math.floor(xRescale.domain()[1])))
                    filtered = _.filter(data, d => ((d.Date >= xmin) && (d.Date <= xmax)))
                    minP = +d3.min(filtered, d => d.Low)
                    maxP = +d3.max(filtered, d => d.High)
                    buffer = (maxP - minP) * 0.1
                    // buffer = Math.floor((maxP - minP) * 0.1)

                yScale.domain([minP - buffer, maxP + buffer])
            }
		}
		else {
			var maxP = 0;
			var minP = 1000000000;
			indicators_info.forEach( function( v, k, m ) {
				var nmaxP = d3.max(v.data, function(d) { return d3.max(_.filter(d.y, (d, i) => i >= Math.floor(xRescale.domain()[0]) && i <= Math.ceil(xRescale.domain()[1]))); });
				var nminP = d3.min(v.data, function(d) { return d3.min(_.filter(d.y, (d, i) => i >= Math.floor(xRescale.domain()[0]) && i <= Math.ceil(xRescale.domain()[1]))); });
				maxP = Math.max(nmaxP, maxP);
				minP = Math.min(nminP, minP);
			});
			var buffer = (maxP - minP) * 0.1;

			yScale.domain([minP - buffer, maxP + buffer])
		}
	}

    function drawGrid() {
		// draw cross y grid

		if(panelType == EPISEC_INDICATOR_PANEL) {
			cgY = gPanel.append("g")
				.attr("class", "axis grid")
				.attr("transform", "translate(" + w + ",0)")
				.call(d3.axisLeft()
					.scale(yScale)
					.tickFormat("")
					.tickSize(w)
					.ticks(6));
		}
		else {
			cgY = gPanel.append("g")
				.attr("class", "axis grid")
				.attr("transform", "translate(" + w + ",0)")
				.call(d3.axisLeft()
					.scale(yScale)
					.tickFormat("")
					.tickSize(w));
		}
    }
    
    function prepareAxis() {
		yAxis = d3.axisRight()
				.scale(yScale);
		
		if(panelType == EPISEC_INDICATOR_PANEL) {
			yAxis.ticks(6);
		}
	}

	d3.selection.prototype.last = function() {
		var last = this.size() - 1;
		return d3.select(this[last]);
	};

	d3.selection.prototype.first = function() {
		return d3.select(this[3]);
	};

	function changeFirstAndLastTickPos() {
		var ltickLabel = gY.select(".tick:last-child").select("text");
		ltickLabel.attr('transform', 'translate(0, 10)');
	}
    
    function drawAxis() {
		
		gY = gPanel.append("g")
				.attr("class", "axis y-axis")
				.attr("transform", "translate(" + w + ",0)")
				.call(yAxis);	

		changeFirstAndLastTickPos();
    }

    function drawFocus() {
		
		//// draw focus yticktext price
		movingytick = gY.append("g")
		   .attr("class", "focusbandtitle")
		
		//get division height in x axis
		linelen = gY.select(".tick line").attr("x2");
		
		movingytickrect = movingytick.append("rect")
			.attr("class", "focusbandtitle")
			.attr("x", linelen)
			.attr("y", -7)
			.attr("width", 45)
			.attr("height", 14)
		movingyticktext = movingytick.append("text")
			.attr("class", "focusbandtitle")
			.attr("x", parseInt(linelen)+3)
			.attr("y", 3);
    }
    
    function doMouseMove(e) {
		var obj = $("#episecpanelrect_" + widgetid + "_" + trade_id);
		var chartposition = obj.position();
		var chartwidth = obj.width();
		var chartheight = obj.height();
		if(e.x >= chartposition.left && e.x <= chartposition.left + chartwidth && e.y >= chartposition.top && e.y <= chartposition.top + chartheight) {
			yband.classed("hoved", true);
			movingytickrect.classed("hoved", true)
			movingyticktext.classed("hoved", true)
			if(panelType == EPISEC_MAIN_PANEL){
				focusPanelCallback('main');
			}
			else{
				focusPanelCallback(trade_id);
			}
		}
		else{
			movingytickrect.classed("hoved", false)
			movingyticktext.classed("hoved", false)
			yband.classed("hoved", false);
		}
	}
    
    this.changeYFocus = function(my){
		var cy = my - y;
        yband.attr("y1",cy)
            .attr("y2",cy)
                
        var focuspricestr = parseFloat(yScale.domain()[1] - cy/h * (yScale.domain()[1] - yScale.domain()[0])).toFixed(2);
		movingytick.attr("transform", "translate(0," + cy + ")")
		movingyticktext.text(focuspricestr)
    };
    
    function drawPanel() {				//main draw function
		prepareScale();

		gPanel = svg.append("g")
					.attr("class", "panel")
					.attr("transform", "translate(" + x + "," + y + ")");

		prepareAxis();
		drawAxis();

		clip = gPanel.append("defs")
		   .append("clipPath")
		   .attr("id", "clip" + widgetid + "_" + trade_id)

		gRect = clip.append("rect")
					.attr("id","episecpanelrect_" + widgetid + "_" + trade_id)
					.attr("width", w)
					.attr("height", h)
					.style("fill", "none")
					.style("pointer-events", "all")
		         
		drawGrid();
		drawFocus();
		window.addEventListener('mousemove', doMouseMove);
		window.addEventListener('click', doMouseDown);
		createBand();
		createChartBody();
		createInfoBars();
		drawChartBody();
		
		createShapeBody();
		createSignalBody();
    }
    
    this.zoom = function(xScaleZ, k) {
        xRescale = xScaleZ;
        tk = k;

		prepareRescale();
		
		// change cross y grid
		if(panelType == EPISEC_INDICATOR_PANEL) {
			cgY.call(d3.axisLeft()
				.scale(yScale)
				.tickFormat("")
				.tickSize(w)
				.ticks(6));
			gY.call(d3.axisRight().scale(yScale).ticks(6));
		}
		else {
			cgY.call(d3.axisLeft()
				.scale(yScale)
				.tickFormat("")
				.tickSize(w));
			gY.call(d3.axisRight().scale(yScale));
		}

		changeFirstAndLastTickPos();

		movingytick.raise();

        drawChartBody();
		drawShapes();
		drawSignals();
    };

    // Define responsive behavior
	this.move = function(left,top,width,height,xScaleZ, xBandZ, xBandvZ, xBandnpZ){
		x = left;
		y = top;
		w = width;
		h = height;

		gPanel.attr("transform", "translate(" + x + "," + y + ")");
	
		// Update the range of the scale with new width/height
		xRescale = xScaleZ;
		xBand = xBandZ;
		xBandv = xBandvZ;
		xBandnp = xBandnpZ;

		prepareScale();
		prepareAxis();
		// Update the axis and text with the new scale
		gY.attr("transform", "translate(" + w + ",0)").call(yAxis);
		
		// change cross y grid
		if(panelType == EPISEC_INDICATOR_PANEL){
			cgY.attr("transform", "translate(" + w + ",0)")
			.call(d3.axisLeft()
			.scale(yScale)
			.tickFormat("")
			.tickSize(w)
			.ticks(6));
		}
		else {
			cgY.attr("transform", "translate(" + w + ",0)")
			.call(d3.axisLeft()
			.scale(yScale)
			.tickFormat("")
			.tickSize(w));
		}
		
		changeFirstAndLastTickPos();

		movingytick.raise();

		gRect.attr("width", w)
			.attr("height", h)

		yband.attr("x2", w)

		drawChartBody();
		drawShapes();
		drawSignals();
	};

	function filterIndDataByDate(inddata) {
		var filtered = [];
		for(var i=0; i<inddata.x.length; i++) {
			var dt = dateFormat(inddata.x[i]);
			var index = indexOfDates(dt, dates);
			if(index != -1) {
				filtered.push({
					Date : inddata.x[i],
					x : index,
					y : inddata.y[i]
				});
			}
		}
		return filtered;
	}
	function formatIndDataByDate(inddata) {
		var filtered = filterIndDataByDate(inddata);
		var refiltered = [];
		for(var i=0; i<filtered.length - 1; i++) {
			refiltered.push( {
				Date : filtered[i].Date,
				x1 : filtered[i].x,
				x2 : filtered[i + 1].x,
				y1 : filtered[i].y,
				y2 : filtered[i + 1].y
			} );
		}
		return refiltered;
	}

	function createIndicators() {							// create all indicator body
		infoids = [];
		indicators_info.forEach( function( v, k, m ) {
			createIndicator(v.data, v.name, k);
		});
	}

	function createIndicator(inddata, name, id){			// create indicator body
		// draw volume bars
		var gInds = chartBody.append("g")
					.attr("class", "indicators");
		
		var curinds = new Map();
		for(var i=0; i<inddata.length; i++){		// maybe inddata is more than 2 ex. aroon up, down
			if(inddata[i].type == 'line') {
				var name = inddata[i].name;
				var filtered = formatIndDataByDate(inddata[i]);
				var curind = gInds.selectAll("."+name)
					.data(filtered)
					.enter()
					.append("line")
					.attr("class", name);

				curinds.set(name, curind);		// linename : graph
			}
			else if(inddata[i].type == 'histogram') {
				var name = inddata[i].name;
				var filtered = filterIndDataByDate(inddata[i]);
				var curind = gInds.selectAll("."+name)
					.data(filtered)
					.enter()
					.append("rect")
					.attr("class", name);

				curinds.set(name, curind);		// typename : graph
			}
		}
		
		gIndicators.set( id , gInds );
		indicators.set( id , curinds );
	}

	this.removeIndicators = function() {
		indicators_info.forEach( function(v, k, m) {
			removeIndicator(k);
		});
	}

	function removeIndicator(id) {
		gIndicators.get(id).remove();
		gIndicators.delete(id);
		indicators.delete(id);
		indicators_info.delete(id);
		removeInfobar(id);
	}

	function drawIndicator(id){
		var curinddata = indicators_info.get(id).data;

		for(var i=0; i<curinddata.length; i++) {
			var name = curinddata[i].name;
			var type = curinddata[i].type;

			if(type == 'line') {
				indicators.get(id).get(name).attr("x1", d => xRescale(d.x1))
					.attr("y1", d => yScale(d.y1))
					.attr("x2", d => xRescale(d.x2))
					.attr("y2", d => yScale(d.y2));
			}
			else if(type == 'histogram') {
				indicators.get(id).get(name).attr("x", d => xRescale(d.x) - xBandv.bandwidth()*tk/2)
					.attr("y", d => d.y >= 0 ? yScale(d.y) : yScale(0))
					.attr("width", xBandv.bandwidth()*tk)
					.attr("height", d => d.y >= 0 ? yScale(0) - yScale(d.y) : yScale(d.y) - yScale(0))
					.attr("class", d => d.y >= 0 ? name + " bullish" : name + " bearish");
			}
		}
	}

	function drawIndicators() {
		indicators_info.forEach( function( v, k, m ) {
			drawIndicator(k);
		});
	}

	this.addIndicator = function(inddata, name, id, tii_id) {
		var newinddata = { id: id, name: name, data: inddata, tii_id:tii_id};
		indicators_info.set(id, newinddata);

		createIndicator(inddata, name, id);
		drawIndicator(id);

		createInfobar(name, inddata, id);
	};

	function close() {
		gPanel.remove();
		window.removeEventListener('mousemove', doMouseMove);
		window.removeEventListener('click', doMouseDown);
		removePanelCallback(trade_id);
	}

	this.closePanel = function() {
		gPanel.remove();
		window.removeEventListener('mousemove', doMouseMove);
		window.removeEventListener('click', doMouseDown);
	}

	function createInfobar(name, ind, id) {
		
		infoids.push(id);
		var cnt = infoids.length;
		var infobar = chartBody.append("g")
						.attr("class", "infobar")
						.attr("transform", "translate(10, " + (10 + 20 * cnt) + ")");

		// close button
		var closebutton = infobar.append('image')
						.attr("id", "close_" + id)
						.attr("xlink:href", '/static/js/episecchart/images/close.svg')
						.attr("width", 15)
						.attr("height", 15)
						.attr("y", -11)

		// setting button
		var settingbutton = infobar.append('image')
						.attr("id", "setting_" + id)
						.attr("xlink:href", '/static/js/episecchart/images/setting.svg')
						.attr("x", 17)
						.attr("width", 15)
						.attr("height", 15)
						.attr("y", -11)

		// add button
		var addbutton = infobar.append('image')
						.attr("id", "add_" + id)
						.attr("xlink:href", '/static/js/episecchart/images/add.svg')
						.attr("x", 35)
						.attr("width", 15)
						.attr("height", 15)
						.attr("y", -11)

		var infovalue = new Map();
		if(id == 'main') {

			infobar.append("text")
					.text(asset + " " + EPISEC_CHARTTYPES[chartType])
					.attr('x', 53);

			var val = infobar.append('text')
							.attr('x', 370);
			infovalue.set('main', val);
		}
		else {

			infobar.append("text")
					.text(name)
					.attr('x', 53)

			for(var i=0; i<ind.length; i++) {
				var val = infobar.append('text')
								.attr("class", ind[i].name + " nostroke")
								.attr('x', 370 + i * 120);
				infovalue.set(ind[i].name, val);
			}
		}
		gInfoBars.set(id, infobar);
		closebuttons.set(id, closebutton);
		infovalues.set(id, infovalue);
	}

	function removeInfobar(id) {
		gInfoBars.get(id).remove();
		gInfoBars.delete(id);

		var index = infoids.indexOf(id);
		for(var i=index + 1; i<infoids.length; i++) {
			gInfoBars.get(infoids[i]).attr("transform", "translate(10," + (10 + 20 * i) + ")");		// up shift
		}
		infoids.splice(index, 1);
	}

	function doMouseDown(e) {
		for(var i=0; i<infoids.length; i++) {
			var curid = infoids[i];
			var obj = $("#close_" + curid);
			var pos = obj.position();
			var wid = obj.width();
			var hei = obj.height();
			if(e.x >= pos.left && e.x <= pos.left + wid && e.y >= pos.top && e.y <= pos.top + hei) {
				if(infoids[i] != 'main') {
					let keys = Array.from( indicators_info.keys() );
					var kindex = keys.indexOf(curid);

					if( kindex == 0 ) {
						if(panelType != EPISEC_MAIN_PANEL){
							close();
						}
						else{
							for(var ii=kindex; ii<keys.length; ii++){
								removeIndicator(keys[ii]);
							}
							removePanelCallback(trade_id);
							trade_id = 0;
						}
					}
					else{
						for(var ii=kindex; ii<keys.length; ii++){
							removeIndicator(keys[ii]);
							removeIndicatorCallback(trade_id, keys[ii]);	
						}
					}
				}
				return;				
			}

			obj = $("#setting_" + curid);
			pos = obj.position();
			wid = obj.width();
			hei = obj.height();
			if(e.x >= pos.left && e.x <= pos.left + wid && e.y >= pos.top && e.y <= pos.top + hei) {
				if(curid != 'main') {
					var tii_id = indicators_info.get(curid).tii_id;
					settingViewCallback(tii_id);
				}
				else {
					settingViewCallback('main');
				}
				return;
			}

			obj = $("#add_" + curid);
			pos = obj.position();
			wid = obj.width();
			hei = obj.height();
			if(e.x >= pos.left && e.x <= pos.left + wid && e.y >= pos.top && e.y <= pos.top + hei) {
				if(trade_id == 0){// this means that add indicator to the main panel firstly
					requireAddIndicatorCallback(trade_id, 1);
				}
				else{
					requireAddIndicatorCallback(trade_id, 0);
				}
			}
		}
	}

	function indexOfSDates(curdate, alldates) {
		var index = -1;
		for(var j=0; j<alldates.length; j++) {
			var dt = dateFormat(alldates[j]);
			if(dt.getTime() == curdate.getTime()) {
				index = j;
				break;
			}
		}
		return index;
	}

	function indexOfDates(curdate, alldates) {
		var index = -1;
		for(var j=0; j<alldates.length; j++) {
			if(alldates[j].getTime() == curdate.getTime()) {
				index = j;
				break;
			}
		}
		return index;
	}

	function drawInfobar(id, curdate, index) {
		if(id == 'main') {
			if(chartType == EPISEC_CANDLESTICK || chartType == EPISEC_BAR || chartType == EPISEC_HEIKINASHI) {
				if(data[index].Open < data[index].Close) {
					infovalues.get(id).get(id).attr("class", "fillbullish");
				}
				else{
					infovalues.get(id).get(id).attr("class", "fillbearish");
				}
				infovalues.get(id).get(id).text("O" + data[index].Open.toFixed(2)
										+ " H" + data[index].High.toFixed(2)
										+ " L" + data[index].Low.toFixed(2)
										+ " C" + data[index].Close.toFixed(2));
			}
			else if(chartType == EPISEC_LINEBREAK || chartType == EPISEC_RENKO) {
				infovalues.get(id).get(id).attr("class", "fill" + data[index].Trending);

				infovalues.get(id).get(id).text("O" + data[index].Trending == 'bullish' ? data[index].Low.toFixed(2) : data[index].High.toFixed(2)
										+ " H" + data[index].High.toFixed(2)
										+ " L" + data[index].Low.toFixed(2)
										+ " C" + data[index].Trending == 'bullish' ? data[index].High.toFixed(2) : data[index].Low.toFixed(2));
			}
			else if(chartType == EPISEC_KAGI){
				
				var filtered = _.filter( data, d => d.toDate == curdate)[0];
				infovalues.get(id).get(id).attr("class", "fill" + filtered.Trending);

				infovalues.get(id).get(id).text("O" + filtered.Trending == 'bullish' ? Math.min(filtered.toClose.toFixed(2), filtered.fromClose.toFixed(2)) : Math.max(filtered.toClose.toFixed(2), filtered.fromClose.toFixed(2))
										+ " H" + Math.max(filtered.toClose.toFixed(2), filtered.fromClose.toFixed(2))
										+ " L" + Math.min(filtered.toClose.toFixed(2), filtered.fromClose.toFixed(2))
										+ " C" + filtered.Trending == 'bullish' ? Math.max(filtered.toClose.toFixed(2), filtered.fromClose.toFixed(2)) : Math.min(filtered.toClose.toFixed(2), filtered.fromClose.toFixed(2)));
			}
		}
		else {
			var inddata = indicators_info.get(id).data;
			for(var i=0; i<inddata.length; i++){		// maybe inddata is more than 2 ex. aroon up, down
				var idata = inddata[i];
				var name = idata.name;
				var type = idata.type;
				var index1 = indexOfSDates(curdate, idata.x);
				if(index1 != -1) {
					infovalues.get(id).get(name).text(name + idata.y[index1].toFixed(3));

					// histogram case
					if(type == 'histogram'){
						if(idata.y[index1] >= 0) {
							infovalues.get(id).get(name).attr("class", "fillbullish");
						}
						else{
							infovalues.get(id).get(name).attr("class", "fillbearish");
						}
					}
				}
			}
		}
	}

	this.drawInfoBar = function(curdate, index) {
		if(panelType == EPISEC_MAIN_PANEL) {
			drawInfobar('main', curdate, index);	
		}
		indicators_info.forEach( function( v, k, m) {
			drawInfobar(k, curdate, index);
		});
	}

	function createInfoBars() {
		if(panelType == EPISEC_MAIN_PANEL) {
			createInfobar('main', null, 'main');
		}
		indicators_info.forEach( function( v, k, m) {
			createInfobar(v.name, v.data, k);
		});
	}

	this.changePanelId = function(id) {
		trade_id = id;
		gRect.attr("id","episecpanelrect_" + widgetid + "_" + trade_id)
	}

	function reenterIndicator(indid, indname, inddata){
		var gInds = gIndicators.get(indid)

		for(var i=0; i<inddata.length; i++){		// maybe inddata is more than 2 ex. aroon up, down
			if(inddata[i].type == 'line') {
				var name = inddata[i].name;
				var filtered = formatIndDataByDate(inddata[i]);
				var curind = gInds.selectAll("."+name)
					.data(filtered);	
			}
			else if(inddata[i].type == 'histogram') {
				var name = inddata[i].name;
				var filtered = filterIndDataByDate(inddata[i]);
				var curind = gInds.selectAll("."+name)
					.data(filtered)

				curinds.set(name, curind);		// typename : graph
			}
		}
	}

	this.setIndicator = function(newindicators) {
		indicators_info = new Map(); 	// indicatorid:{id,name,data}
	
		for(var i=0; i<newindicators.length; i++)	{
			indicators_info.set(newindicators[i].id, {
				id : newindicators[i].id,
				name : newindicators[i].name,
				data : newindicators[i].data,
				tii_id : newindicators[i].tii_id
			});

			var inddata = newindicators[i].data;
			var indid = newindicators[i].id;
			var indname = newindicators[i].name;
			reenterIndicator(indid, indname, inddata);
			drawIndicator(indid);
		}		
	}
	drawPanel();
};