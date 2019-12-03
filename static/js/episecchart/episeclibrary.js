function atr(prices, atrlength){
    if(atrlength == undefined) {
		atrlength = 14;
	}
	//atr algorithm
	var atrarr = [];
	var atr=[];
	var tri = [];
	var dates = [];

	var fromindex = 0;
	var toindex = 0;
	atr.push(0);
	
	//calculate tr
	tri.push(prices[0]['High'] - prices[0]['Low']);
	for(var i=1; i<prices.length; i++){
		tr = Math.max(prices[i]['High'] - prices[i]['Low'], Math.abs(prices[i]['High'] - prices[i-1]['Close']));
		tr = Math.max(tr, Math.abs(prices[i]['Low'] - prices[i-1]['Close']));
		tri.push(tr);
	}

	//calculate first atr. simply first 14 tr average
	atr[0] = _.sum(_.filter(tri, (d, i) => i < atrlength)) / atrlength;

	//calculate atr

	var atrindex = 1;
	for(var t=atrlength; t<tri.length; t++) {
		atr[atrindex] = (atr[atrindex - 1] * (atrlength - 1) + tri[t]) / atrlength;
		atrindex++;
	}

	return atr;
}

// This function applies the kagi algorithm to figure out the trends
function preprocess_data_kagi(data, reversalType, reversalValue){

	var trends = new Array();

	// Initialize the output data
	var output_data = [];

	var counter = 0;
	var trend;
	var j = 0;

	// Pushing the first data point as first day's close
	output_data.push({x:0,Close:data[0].Close,Date:data[0].Date});

	var broke_at = 0;

	// Make a copy of the data set to work upon.
	var temp_array = data.slice();

	// Figure out the "initial trend" in data to figure out the direction, thickness, color of line etc
	for(var k=1;k<temp_array.length;k++){
		var diff = temp_array[k].Close - temp_array[k-1].Close;
		if (diff>0){
			trend = '+';
			broke_at = k;
			break;
		}else if(diff<0){
			trend = '-';
			broke_at = k;
			break;
		}else{
			continue;
		}
	}

	// The first trend is initialized in the trends array based on the above iteration.
	trends[0] = trend;

	// We will slice the dataset from the value of the first change in trend above.
	var data = data.slice(broke_at-1);

	// Initializing the last_close variable to that of the dataset's first datapoint.
	var last_close = data[0].Close;

	// Now the magic!
	for(var i=1; i<data.length; i++){
	var diff = data[i].Close - last_close;

	if (diff>0){
			trend = '+'; // It is positive
	}else if(diff<0){
			trend = '-'; // It is negative
	}else if(diff==0){
			trend = trends[i-1]; // Values seem equal. Continue the previous trend.
	}

	// Set current trend to that of calculated above.
	trends[i] = trend;

	var value_to_compare = 0;
	if(reversalType.localeCompare("diff") == 0){
		value_to_compare = diff; // If reversalType is difference then just have to compare the change in value
	}else{
		value_to_compare = diff/last_close * 100; // If reversalType is pct then compute the change in value and compare
	}

	// If the absolute value of change (be it difference or percentage) is greater than the configured reversal_value
	if (Math.abs(value_to_compare) >= reversalValue){
		// means there is a change in trend. time to move along the x axis
		if(trends[i] != trends[i-1]){
			counter = counter+1;
			// Push the last_close at the new x position so a |_| or |-| kind of graph.
			output_data.push({x:counter,Close:last_close,Date:data[i].Date});
			// Push the new close at the new x position
			output_data.push({x:counter,Close:data[i].Close,Date:data[i].Date});
		}
		// means there is no change in trend. time to move along the y axis (upward or downward)
		else{
				if(trends[i]=='+' && data[i].Close>data[i-1].Close){
					output_data.push({x:counter,Close:data[i].Close,Date:data[i].Date});
				}
				else if(trends[i]=='-' && data[i].Close < data[i-1].Close){
					output_data.push({x:counter,Close:data[i].Close,Date:data[i].Date});
				}
			}
		last_close = data[i].Close;
		j=0;
	}else{
			if(trends[i]==trends[i-1]){
				// If the trend is the same and the last_close values are conforming to the trend, then
				// push to output_data in a way that it extends along the y axis on the same x axis point (counter).
				if(trends[i]=='+' && data[i].Close>data[i-1].Close){
					output_data.push({x:counter,Close:data[i].Close,Date:data[i].Date});
				}
				else if(trends[i]=='-' && data[i].Close < data[i-1].Close){
					output_data.push({x:counter,Close:data[i].Close,Date:data[i].Date});
				}
				// Safe to set the last_close here as it is an actual point added to output_data.
				last_close = data[i].Close;
				// Reset the interim j variable to 0
				// Means the original dataset and output_data set are back in sync.
				j=0;
			}else{
				// This is to ignore minor variations in the stock values. We reset the last_close and current trend
				// every time this piece of code gets executed.
				// In Kagi charts, minor fluctuations are ignored while plotting.
				// The output_data set and the original dataset are out of sync till j != 0.
				last_close = data[i-1-j].Close;
				trends[i] = trends[i-1-j];
				j+=1;
			}
		}
	}
	return output_data;
}

function filter_same_x_points_from_data(data){
	var filtered_data = [];

	// Push the first datapoint
	filtered_data.push(data[0]);

	// If there are multiple points with the same x coordinate then filter the dataset to
	// have only the first and the last x position (highest and lowest last_close position)
	// This will remove considerable no. of points
	for(var i=1; i<data.length; i++){
		if(data[i].x == data[i-1].x){
			// ignore these points. this was exactly the purpose of this filtering function.
		}else{
			filtered_data.push(data[i-1]);
			filtered_data.push(data[i]);
		}
	}

	// Push the last datapoint
	filtered_data.push(data[data.length-1]);
	return filtered_data;
}

// This function add the points which are at the shoulders and bases (useful only during change of trends).
function add_base_shoulder_points(data){
	var base;
	var shoulder;
	var uptrend;

	// Deciding the initial trend in dataset based on which the base and shoulders are decided.
	if(data[1].Close >= data[0].Close){
		base = data[0].Close;
		shoulder = data[1].Close;
		uptrend=true;
	}else{
		base = data[1].Close;
		shoulder = data[0].Close;
		uptrend=false;
	}

	var points_to_add=[]; // abstracted out so can be used if needed.
	var positions_to_add_to = []; // abstracted out so can be used if needed.

	for(var i=0; i<data.length;i++){

		if(uptrend && data[i].Close < base){
			// to_break:true is an identifier that the lines need to change their formatting beyond this point.
			points_to_add.push({Date:data[i].Date,Close:base,x:data[i].x,to_break:true});
			positions_to_add_to.push(i);
			uptrend = !uptrend;
		}
		else if(!uptrend && data[i].Close > shoulder){
			// to_break:true is an identifier that the lines need to change their formatting beyond this point.
			points_to_add.push({Date:data[i].Date,Close:shoulder,x:data[i].x,to_break:true});
			positions_to_add_to.push(i);
			uptrend = !uptrend;
		}

		// Update the base and the shoulders while traversing the array.
		if(i>0 && data[i].Close > data[i-1].Close){
			base = data[i-1].Close;
			shoulder = data[i].Close;

		}else if(i>0 && data[i].Close < data[i-1].Close){
			base = data[i].Close;
			shoulder = data[i-1].Close;
		}
	}

	// Based on the points generated above and their positions,
	// actually add these points into the dataset for final yang-ying generation
	for(var k=0; k<positions_to_add_to.length; k++){
		// the +k is to encounter dynamic increase in the dataset's size.
		// The points_to_add need to be added at the correct position in the data array.
		data.splice(positions_to_add_to[k]+k,0,points_to_add[k]);
	}

	return data;
}


// This function makes the dataset which is fed to the d3.js library to render as svg
// Here, based on to_break metric, formatting options like thickness, colors are added.
function generate_yang_ying_lines(data){

	var output_array_of_lines = [];
	var start_position = 0;
	var break_position = 0;
	var uptrend;

	// Find the initial trend in data. In this case if its equal then I'm considering it as
	// positive.
	if(data[1].Close >= data[0].Close){
		uptrend = true;
	}else{
		uptrend = false;
	}

	var linedata = [];
	var datearray = [];
	// if the key "to_break" is true, then group the lines and add their formatting.
	for(var i=1;i<data.length;i++){
		if(data[i-1].x != data[i].x) {
			linedata.push({
				fromDate : data[i-1].Date,
				toDate : data[i].Date,
				x1 : data[i-1].x,
				x2 : data[i].x,
				fromClose : data[i].Close,
				toClose : data[i].Close,
				Type : 'h',
				Trending : uptrend ? 'bullish' : 'bearish'
			});
			datearray.push(data[i-1].Date);
		}
		else {
			linedata.push({
				fromDate : data[i-1].Date,
				toDate : data[i].Date,
				x : data[i].x,
				fromClose : data[i-1].Close,
				toClose : data[i].Close,
				Type : 'v',
				Trending : uptrend ? 'bullish' : 'bearish'
			});

			if('to_break' in data[i]){
				uptrend = !uptrend;
			}
		}
		// if('to_break' in data[i]){
		// 	var temp_array = data.slice();
		// 	break_position = i;
		// 	var lines = temp_array.splice(start_position,break_position-start_position+1);
		// 	start_position = break_position;
		// 	output_array_of_lines.push({uptrend:uptrend,p:lines});
		// 	uptrend=!uptrend;
		// }
	}
	datearray.push(data[data.length-1].Date);

	// adding the last set of lines.
	// var temp_array = data.slice();
	// var final_section_after_break = temp_array.splice(start_position);
	// output_array_of_lines.push({uptrend:uptrend,p:final_section_after_break});

	return {kagidata:linedata, dates:datearray};
}

function kagi(prices) {
	var reversalValue = atr(prices)[0];
	
	// Preprocess the data and generate the initial set of coordinates which have to be plotted.
	// var pre_processed_data = preprocess_data(inputData,reversalType,reversalValue);
	var pre_processed_data = preprocess_data_kagi(prices,'diff',reversalValue);
	
	// Filter the preprocessed data to remove the points with same x coordinate except the min and max
	var filtered_data = filter_same_x_points_from_data(pre_processed_data);

	// Add additional points for formatting the yang-ying lines at the base and shoulders.
	var formatted_data = add_base_shoulder_points(filtered_data);

	 // Group the lines into a set with its formatting based on break points computed in add_base_shoulder_points().
	var data_to_display = generate_yang_ying_lines(formatted_data);

	return data_to_display;
}

function linebreak(prices, linecount = 3) {
	closes = _.map(prices, 'Close');
	dates = _.map(prices, 'Date');
	var index = 1;
	var prevhigh = closes[0];
	var prevlow = closes[0];
	var lines = [];

	while(index<closes.length){
		var nowclose = closes[index];
		var nowdate = dates[index];
		
		for(var i=lines.length-1; i>=lines.length-linecount+1 && i>=0; i--) {
			prevhigh = Math.max(prevhigh, lines[i].High);
			prevlow = Math.min(prevlow, lines[i].Low);
		}

		var prevhigh1;
		var prevlow1;
		if(index==1) {
			prevhigh1 = closes[0];
			prevlow1 = closes[0];
		}
		else {
			prevhigh1 = lines[lines.length-1].High;
			prevlow1 = lines[lines.length-1].Low;
		}

		if(nowclose > prevhigh) {
			//adding brick
			lines.push({
				Low : prevhigh1,
				High : nowclose,
				Date : nowdate,
				Trending : 'bullish'
			});
			prevhigh = nowclose;
			prevlow = prevhigh1;
		}
		else if(nowclose < prevlow) {
			//adding brick
			lines.push({
				Low : nowclose,
				High : prevlow1,
				Date : nowdate,
				Trending : 'bearish'
			});
			prevhigh = prevlow1;
			prevlow = nowclose;
		}
		index++;
	}

	return lines;
}

function renko(prices, atrlength) {
	if(atrlength == undefined) {
		atrlength = 14;
	}
	bricksize = atr(prices,atrlength)[0];

	closes = _.map(prices, 'Close');
	dates = _.map(prices, 'Date');
	var index = 1;
	var prevhigh = closes[0];
	var prevlow = closes[0];
	var prevdate = dates[0];

	var bricks = [];

	while(index<closes.length){
		var nowclose = closes[index];
		var nowdate = dates[index];
		if(nowclose > prevhigh && nowclose - prevhigh > bricksize) {
			var newbrickcount = Math.round(Math.abs(nowclose - prevhigh) / bricksize);
			var dateoffset = nowdate.getTime() - prevdate.getTime();
			var cclose = prevhigh;
			for(var i = 0; i < newbrickcount; i++)  {
				var cdate = new Date(prevdate.getTime() + Math.round(dateoffset * i / newbrickcount));
				
				//adding brick
				bricks.push({
					Low : cclose,
					High : cclose + bricksize,
					Date : cdate,
					Trending : 'bullish'
				});
				cclose += bricksize;
			}
			prevhigh = cclose;
			prevlow = cclose - bricksize;
			prevdate = nowdate;
		}
		else if(nowclose < prevlow && prevlow - nowclose > bricksize) {
			var newbrickcount = Math.round(Math.abs(nowclose - prevlow) / bricksize);
			var dateoffset = nowdate.getTime() - prevdate.getTime();
			var cclose = prevlow;
			for(var i = 0; i < newbrickcount; i++)  {
				var cdate = new Date(prevdate.getTime() + Math.round(dateoffset * i / newbrickcount));
				
				//adding brick
				bricks.push({
					Low : cclose - bricksize,
					High : cclose,
					Date : cdate,
					Trending : 'bearish'
				});
				cclose -= bricksize;
			}
			prevlow = cclose;
			prevhigh = cclose + bricksize;
			prevdate = nowdate;
		}
		index++;
	}

	return {BrickSize : bricksize, Bricks : bricks};
}