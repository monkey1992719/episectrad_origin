const EPISEC_MONTHS = {0 : 'Jan', 1 : 'Feb', 2 : 'Mar', 3 : 'Apr', 4 : 'May', 5 : 'Jun', 6 : 'Jul', 7 : 'Aug', 8 : 'Sep', 9 : 'Oct', 10 : 'Nov', 11 : 'Dec'}
const EPISEC_CHARTTYPES = ['CandleStick', 'Bar', 'Renko', 'Heikin Ashi', 'Line break', 'Kagi'];
const EPISEC_CANDLESTICK = 0;
const EPISEC_BAR = 1;
const EPISEC_RENKO = 2;
const EPISEC_HEIKINASHI = 3;
const EPISEC_LINEBREAK = 4;
const EPISEC_KAGI = 5;

const EPISEC_MAIN_PANEL = 1;
const EPISEC_INDICATOR_PANEL = 2;


var EpisecChart = function(options) {
	var widgetid = Math.floor(Math.random()*10000000);
	var chartType = options.chartType;
	var width = options.width;
	var height = options.height;
	var prices = options.data;
	var containerId = options.container;
	var removeIndicatorCallback = options.removeIndicatorCallback;
	var removePanelCallback = options.removePanelCallback;
	var settingViewCallback = options.settingViewCallback;
	var requireAddIndicatorCallback = options.requireAddIndicatorCallback;
	var bandOverCallback = options.bandOverCallback;
	var preyear;
	var premonth;
	var bIntraday = options.bIntraday;

	var trades = new Map();

	var nowt;	//now transform

	if('fullscreen' in options && options.fullscreen) {
		width = $('#'+containerId).width();
		height = $('#'+containerId).height();
		d3.select(window).on('resize', this.resize);
	}

	var margin = {top: 0, right: 70, bottom: 30, left: 0};
	var dateFormat;
	var symbol = options.symbol;
	var asset = symbol + " " + options.asset;

	function validateData() {
		if(bIntraday) {
			dateFormat = d3.timeParse("%Y-%m-%d %H:%M:%S");
		}
		else{
			dateFormat = d3.timeParse("%Y-%m-%d");
		}

		for (var i = 0; i < prices.length; i++) {
			prices[i]['Date'] = dateFormat(prices[i]['Date'])
			prices[i]['Open'] = parseFloat(prices[i]['Open'])
			prices[i]['High'] = parseFloat(prices[i]['High'])
			prices[i]['Low'] = parseFloat(prices[i]['Low'])
			prices[i]['Close'] = parseFloat(prices[i]['Close'])
			// prices[i]['Adj Close'] = parseFloat(prices[i]['Adj Close'])
			prices[i]['Volume'] = parseFloat(prices[i]['Volume'])
		}
	}

	validateData();

	var w = width - margin.left - margin.right;
	var h = height - margin.top - margin.bottom;

	var svg;
	var data;
	var kagidata, bricksize; // special for kagi and renko
	var dates;
	var xScale,xDateScale,xBand,xBandnp,xBandv,xRescale,tk=1;  //tk is zoom scale
	var xAxis, gX, cgX;
	var xband,xbands, gXbands, gXband;
	var movingxtick, movingxtickrect, movingxticktext;
	var widgetrect;
	
	var panelsizes = [[w, h]];

	var gPanels;  // each gPanel has panel information panel(ex. Aroon(14), asset), focus value pane, y focus, region rect, graph type(ex. ind_Aroon), ymin, ymax, gY, css infomation
	var focusedPanel;
	const EPISEC_MAX_PANEL_COUNT = 4;
	const EPISEC_HEIGHT_PERCENT = [[1], [0.7, 0.3], [0.6, 0.2, 0.2],  [0.4, 0.2, 0.2, 0.2]];

	var main_trade_id = 0;
	
	function init() {
		tk=1;
		trades = new Map();
		main_trade_id = 0;
		panelsizes = [[w, h]];
	}

	this.redrawChart = function(newdata, newasset, newsymbol, newbIntraday) {
		prices = newdata;
		symbol = newsymbol;
		asset = symbol + " " + newasset;
		bIntraday = bIntraday;
		removeChart();
		validateData();
		init();
		drawChart();
	}

	this.setChartType = function(n) {
		if(chartType == n) return;
		removeChart();
		chartType = n;
		// init();
		drawChart();
	};

	function removeChart() {
		window.removeEventListener('mousemove', doMouseMove);
		d3.select("#" + containerId)
			.selectAll("svg")
			.remove();
	}

	function createTradingIndicator(tradeid, indicators, cx, cy, cw, ch){	// create a new trade
		var panel = new EpisecChartPanel({
			widgetid : widgetid,
			dates : dates,
			svg : svg,
			indicators_info : indicators,
			width : cw,
			height : ch,
			x : cx,
			y : cy,
			tk : tk,
			trade_id : tradeid,
			chartType : chartType,
			panelType : EPISEC_INDICATOR_PANEL,
			xDateScale : xDateScale,
			xRescale : xRescale,
			xScale : xScale,
			xBand : xBand,
			xBandv : xBandv,
			xBandnp : xBandnp,
			asset : asset,
			removeIndicatorCallback : removeIndicatorHandler,
			removePanelCallback : removePanelHandler,
			focusPanelCallback : focusPanel,
			settingViewCallback : settingViewCallback,
			requireAddIndicatorCallback : requireAddIndicatorCallback,
			dateFormat : dateFormat
		});
		cy += ch;
		gPanels.set(tradeid, panel);
		gXbands.raise();
		return panel;
	}

	this.addTradingIndicator = function(indicators, tradeid, bOrg) {					// add new trade with technical indicator
		trades.set(tradeid, indicators);

		if(bOrg){	// original chart draw
			for(var i=0; i<indicators.length; i++){
				var name = indicators[i].name;
				var id =  indicators[i].id; 
				var inddata = indicators[i].data;
				var tii_id = indicators[i].tii_id;
				gPanels.get('main').addIndicator(inddata, name, id, tii_id);
			}
			gPanels.get('main').changePanelId(tradeid);
			main_trade_id = tradeid;

		}
		else {
			if(gPanels.size == EPISEC_MAX_PANEL_COUNT) {
				alert("Trade count is limited to " + EPISEC_MAX_PANEL_COUNT + "!");
			}
			createTradingIndicator(tradeid, indicators, 0, 0, w, h);
			calculateHeights();
		}
	};

	this.setTradingIndicator = function(indicators, tradeid, bOrg) {					// add new trade with technical indicator
		trades.set(tradeid, indicators);

		if(bOrg){	// original chart draw
			gPanels.get('main').setIndicator(indicators);
		}
		else {
			gPanels.get(tradeid).setIndicator(indicators);
		}
	};

	this.addIndicator = function(inddata, name, id, tradeid, tii_id) {
		trades.get(tradeid).push({id:id, name:name, data:inddata, tii_id:tii_id});
		gPanels.get(tradeid).addIndicator(inddata, name, id, tii_id);
	};

	this.removePanel = function(trade_id) {
		if(main_trade_id == trade_id){
			gPanels.get('main').removeIndicators();
			trades.delete(trade_id);			
		}
		else{
			gPanels.get(trade_id).closePanel();
			trades.delete(trade_id);
			gPanels.delete(trade_id);
			calculateHeights();
		}
	}

	var removePanelHandler = function(id) {
		trades.delete(id);
		gPanels.delete(id);
		calculateHeights();
		removePanelCallback(id);
	}
	
	var removeIndicatorHandler = function(tradeid, id) {
		removeIndicatorCallback(tradeid, id);
	}

	function drawChart() {				//main draw function
		svg = d3.select("#" + containerId)
			.append("svg")
			.attr("class", "episecchart")
			.attr("width", width)
			.attr("height", height)
			.append("g")
		
		svg.append("svg:defs").append("svg:marker")
			.attr("id", "triangle_red")
			.attr("refX", 6)
			.attr("refY", 6)
			.attr("markerWidth", 30)
			.attr("markerHeight", 30)
			.attr("markerUnits","userSpaceOnUse")
			.attr("orient", "auto")
			.append("path")
			.attr("d", "M 0 0 12 6 0 12 3 6")
			.style("fill", "red");
		
		svg.append("svg:defs").append("svg:marker")
			.attr("id", "triangle_green")
			.attr("refX", 6)
			.attr("refY", 6)
			.attr("markerWidth", 30)
			.attr("markerHeight", 30)
			.attr("markerUnits","userSpaceOnUse")
			.attr("orient", "auto")
			.append("path")
			.attr("d", "M 0 0 12 6 0 12 3 6")
			.style("fill", "green");

		data = prepareData();
		dates = getDatesfromData();

		prepareScale();
		prepareAxis();
		drawAxis();
		widgetrect = svg.append("rect")
					.attr("id","episecchartrect" + widgetid)
					.attr("width", w)
					.attr("height", h)
					.style("fill", "none")
					.style("pointer-events", "all")
					.attr("clip-path", "url(#clip" + widgetid + ")")
		drawGrid();
		drawFocus();
		window.addEventListener('mousemove', doMouseMove);
		createBand();
		drawBand();

		gPanels = new Map();

		var panel = new EpisecChartPanel({
			widgetid : widgetid,
			dates : dates,
			data : data,
			indicators_info : new Map(),
			trade_id : main_trade_id,
			width : w,
			height : panelsizes[0][1],
			x : 0,
			y : 0,
			svg : svg,
			chartType : chartType,
			panelType : EPISEC_MAIN_PANEL,
			tk : tk,
			asset : asset,
			xDateScale : xDateScale,
			xRescale : xRescale,
			xScale : xScale,
			xBand : xBand,
			xBandv : xBandv,
			xBandnp : xBandnp,
			removeIndicatorCallback : removeIndicatorHandler,
			settingViewCallback : settingViewCallback,
			removePanelCallback : removePanelHandler,
			focusPanelCallback : focusPanel,
			requireAddIndicatorCallback : requireAddIndicatorCallback,
			dateFormat : dateFormat
		});

		if(main_trade_id != 0) {
			for(var i=0; i<trades.get(main_trade_id).length; i++){
				var name = trades.get(main_trade_id)[i].name;
				var id =  trades.get(main_trade_id)[i].id; 
				var inddata = trades.get(main_trade_id)[i].data;
				gPanels.get('main').addIndicator(inddata, name, id);
			}
			gPanels.get('main').changePanelId(main_trade_id);
		}

		var sumheight = panelsizes[0][1];
		gPanels.set('main', panel);
		gXbands.raise();
		var i=0;
		trades.forEach(function( v, k, m ) {
			if(k != main_trade_id){
				createTradingIndicator(k, v, 0, sumheight, w, panelsizes[i+1][1]);
				sumheight += panelsizes[i+1][1];
				i++;
			}
		});

		const extent = [[0, 0], [w, h]];
		
		var zoom = d3.zoom()
		  .scaleExtent([1, 70])
		  .translateExtent(extent)
		  .extent(extent)
		  .on("zoom", zoomed)

		svg.call(zoom)
	}
	
	function prepareData() {
		let outputdata = prices;
		if(chartType == EPISEC_HEIKINASHI) {
			for (var i = 0; i < prices.length; i++) {
				outputdata[i]['Close'] = (outputdata[i]['Close']+outputdata[i]['Low']+outputdata[i]['High']+outputdata[i]['Open'])/4;
			}
			return outputdata;
		}
		else if(chartType == EPISEC_RENKO){
			var renkodata = renko(outputdata);
			bricksize = renkodata.BrickSize;
			return renkodata.Bricks;
		}
		else if(chartType == EPISEC_LINEBREAK){
			return linebreak(outputdata);
		}
		else if(chartType == EPISEC_KAGI){
			kagidata = kagi(outputdata)
			return kagidata.kagidata;
		}

		return outputdata;
	}

	function getDatesfromData() {
		if(chartType == EPISEC_CANDLESTICK || chartType == EPISEC_BAR || chartType == EPISEC_LINEBREAK || chartType == EPISEC_HEIKINASHI || chartType == EPISEC_RENKO) {
			return _.map(data, 'Date');	
		}
		else if(chartType == EPISEC_KAGI) {
			return kagidata.dates;
		}
		return undefined;
	}

	function prepareScale() {
		xmin = d3.min(dates);
        xmax = d3.max(dates);
		xScale = d3.scaleLinear().domain([0, dates.length])
						.range([0, w]);
		xRescale = xScale;
		xDateScale = d3.scaleQuantize().domain([0, dates.length]).range(dates)
		xBand = d3.scaleBand().domain(d3.range(0, dates.length)).range([0, w]).padding(0.3)
		xBandv = d3.scaleBand().domain(d3.range(0, dates.length)).range([0, w]).padding(0.1)
		xBandnp = d3.scaleBand().domain(d3.range(0, dates.length)).range([0, w])

		if(nowt != undefined) {
			xRescale = nowt.rescaleX(xScale);
			tk = nowt.k;
		}
	}

	function datetickformat(d) {
		var i = d;
		d = parseInt(d);
		if (d >= 0 && d <= dates.length-1) {
			d = dates[d]
			try{
				hours = d.getHours()
				minutes = (d.getMinutes()<10?'0':'') + d.getMinutes() 
			}
			catch(err){
				console.log(err);
			}
			// amPM = hours < 13 ? 'am' : 'pm'
			// return hours + ':' + minutes + amPM + ' ' + d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear()
			var dtstr;

			if(!bIntraday) {
				dtstr = d.getDate() + ' ' + EPISEC_MONTHS[d.getMonth()] + ' ' + d.getFullYear();
			}
			else {
				dtstr = hours + ':' + minutes;
			}

			return dtstr;
		}
		return '';
	}

	function prepareAxis() {
		// drawing axis-x
		xAxis = d3.axisBottom()
				.scale(xScale)
				.tickFormat(datetickformat);
	}

	function drawAxis() {
		gX = svg.append("g")
				.attr("class", "axis x-axis") //Assign "axis" class
				.attr("transform", "translate(0," + h + ")")
				.call(xAxis);
		
		preyear="";

		if(!bIntraday){
			gX.selectAll(".tick text")
				.call(opttimestamp);
		}
	}

	function drawGrid() {
		
		// draw cross x grid
		cgX = svg.append("g")
				.attr("class", "axis grid")
				.attr("transform", "translate(0," + h + ")")
				.call(d3.axisTop()
					.scale(xScale)
					.tickFormat("")
					.tickSize(h));
	}

	
	
	function drawFocus() {
		//// draw focus xticktext date
		movingxtick = gX.append("g")
		   .attr("class", "focusbandtitle")
		
		//get division height in x axis
		var linelen = gX.select(".tick line").attr("y2");
		
		var rectwidth = 60;
		if(bIntraday) {
			rectwidth = 90;
		}

		movingxtickrect = movingxtick.append("rect")
			.attr("class", "focusbandtitle")
			.attr("y", linelen)
			.attr("x", -rectwidth / 2)
			.attr("width", rectwidth)
			.attr("height", 12)
		movingxticktext = movingxtick.append("text")
			.attr("class", "focusbandtitle")
			.attr("y", 15);
	}

	function createBand() { //for the mouse moving event capture
		//make bands per timestamp
		gXbands = svg.append("g")
			.attr("class", "xbands");
  
		xbands = gXbands.selectAll("rect")
			.data(dates)
			.enter().append("rect")
			.attr("class", function(d, i) { return "xband"+i; })
			.attr("y", 0)
			.attr("height", h)

		//make focus xband timestamp
		gXband = svg.append("g")
			.attr("class", "xband");
		xband = gXband.append("line")
			.attr("class", "xband")
			.attr("x1", 0)
			.attr("y1", 0)
			.attr("y2", h)
			.attr("x2", 0)

		xbands.on("mousemove", doBandOver);
	}

	function drawBand() {
		xbands.attr("x", (d, i) => xRescale(i) - (xBand.bandwidth()*tk)/2)
			.attr("width", xBand.bandwidth()*tk)
	}

	function doBandOver(d, i) {
		xband.attr("x1",d3.mouse(this)[0])
				.attr("x2",d3.mouse(this)[0]);
			
		movingxtick.attr("transform", "translate(" + d3.mouse(this)[0] + ")")						
		var focustimestr = d.getDate() + " " + EPISEC_MONTHS[d.getMonth()] + " '" + (d.getFullYear()%100);
		if(bIntraday) {
			var min = d.getMinutes();
			if(min<10) min = "0" + min;
			focustimestr = focustimestr + " " + d.getHours() + ":" + min;
		}
		movingxticktext.text(focustimestr)

		gPanels.forEach(function (v, k, m) {
			v.drawInfoBar(d, i);
		});
		if(focusedPanel != undefined) {
			focusedPanel.changeYFocus(d3.mouse(this)[1]);
		}

		bandOverCallback(d, i);
	}

	function doMouseMove(e) {
		var chartposition = $("#episecchartrect"+widgetid).position();
		var chartwidth = $("#episecchartrect"+widgetid).width();
		var chartheight = $("#episecchartrect"+widgetid).height();
		if(e.x >= chartposition.left && e.x <= chartposition.left + chartwidth && e.y >= chartposition.top && e.y <= chartposition.top + chartheight) {
			xband.classed("hoved", true);
			movingxtickrect.classed("hoved", true)
			movingxticktext.classed("hoved", true)
		}
		else{
			movingxtickrect.classed("hoved", false)
			movingxticktext.classed("hoved", false)
			xband.classed("hoved", false);
		}
	}
	//zoom functions
	function zoomed() {
			
		var t = d3.event.transform;
		tk = t.k;
		nowt = t;
		var xScaleZ = t.rescaleX(xScale);
		xRescale = xScaleZ;

		let hideTicksWithoutLabel = function() {
			d3.selectAll('.xAxis .tick text').each(function(d){
				if(innerHTML === '') {
					parentNode.style.display = 'none'
				}
			})
		}

		//change timeseries
		gX.call(
			d3.axisBottom(xScaleZ).tickFormat(datetickformat)
		)

		//change timestamp series tick text
		preyear="";

		if(!bIntraday){
			gX.selectAll(".tick text")
				.call(opttimestamp);
		}

		// change cross x grid
		cgX.call(d3.axisTop()
				.scale(xScaleZ)
				.tickFormat("")
				.tickSize(h));
	
		hideTicksWithoutLabel();

		movingxtick.raise();
		
		gPanels.forEach(function(value, key, map) {
			value.zoom(xScaleZ, t.k);
		});

		drawBand();
	}

	function opttimestamp(text){
	
		text.each(function() {
			var timeseriesstr;
			var text = d3.select(this),
					words = text.text().split(/\s+/).reverse();
			var year = words[0];
			var month = words[1];
			var day = words[2];
	
			if(preyear=="") {
				timeseriesstr = day;
			}
			else if(year!=preyear){
				timeseriesstr = year;
			}
			else{
				if(month!=premonth){
					timeseriesstr = month;
				}
				else
				{
					timeseriesstr = day;
				}
			}
	
			preyear = year;
			premonth = month;
			preday = day;
				
			text.text(timeseriesstr);
		});
	}

	//calculate height of panels
	function calculateHeights() {
		panelsizes = [];

		var sumheight = 0;
		var i = 0;
		gPanels.forEach( function (v, k, m) {
			var height = EPISEC_HEIGHT_PERCENT[gPanels.size - 1][i]*h;
			v.move(0, sumheight, w, height, xRescale, xBand, xBandv, xBandnp);
			sumheight += height;
			i++;
		});
	}

	// Define responsive behavior
	this.resize = function() {
		var conwidth = parseInt(d3.select("#"+containerId).style("width"));
		var conheight = parseInt(d3.select("#"+containerId).style("height"));
		width = conwidth;
		height = conheight;
		w = width - margin.left - margin.right;
		h = height - margin.top - margin.bottom;

		d3.select("#" + containerId)
			.select("svg")
			.attr("width", width)
			.attr("height", height);

		widgetrect.attr("width", w)
			.attr("height", h);

		clip.attr("width", w)
			.attr("height", h);

		// Update the range of the scale with new width/height
		prepareScale();
		if(nowt != undefined) {
			xRescale = nowt.rescaleX(xScale);
		}
		prepareAxis();

		gX.attr("transform", "translate(0," + h + ")")
			.call(xAxis);

		preyear="";

		if(!bIntraday){
			gX.selectAll(".tick text")
				.call(opttimestamp);
		}
		
		cgX.attr("transform", "translate(0," + h + ")")
			.call(d3.axisTop()
			.scale(xRescale)
			.tickFormat("")
			.tickSize(h));

		movingxtick.raise();
		
		xband.attr("y2", h);

		calculateHeights();
		drawBand();
	};

	this.removeAllShapes = function() {
		gPanels.forEach( function (v, k, m) {
			v.removeAllShapes();
		});
	};

	this.createMultipointShape = function(points, options){
		gPanels.get('main').createMultipointShape(points, options);
	};

	this.createSignalShape = function(data){
		for(var i=0; i<data.length; i++){
			gPanels.get(data[i].id).createSignalShape(data[i]);
		}
	};

	function focusPanel(id) {
		focusedPanel = gPanels.get(id);
	}

	this.setIndicatorSettings = function(settings) {

		// settings.
		// color, width setting
		for(var j=0; j<settings.length; j++) {
			setting = settings[j];
			$("."+setting.plotname).css('fill', setting.color);
			$("."+setting.plotname).css('stroke', setting.color);
			$("."+setting.plotname).css('stroke-width', setting.width);
		}
	}

	drawChart();
};