var rpisURI = location.origin + '/RPis';

function sensorURI(rpiUid) {
	return location.origin + '/Sensors?rpiUid=' + rpiUid;
}

function readingURI(sensorUid) {
	return location.origin + '/SensorReadings?sensorUid=' + sensorUid;
}


var deviceViewModel = {};


/**
 * Add internal configs before observableifying data.
 */
function beforeObservableify(deviceViewModelData) {
	
	// add selected=false keys to rpi and sensors
	for (var i = 0; i < deviceViewModelData['RPis'].length; ++i) {
		var rpi = deviceViewModelData['RPis'][i];
		rpi['selected'] = false;
		for (var j = 0; j < rpi['sensors'].length; ++j) {
			var sensor = rpi['sensors'][j];
			sensor['selected'] = false;
			sensor['readings'] = [];
		}
	}
	
	// add main selected item and type props
	deviceViewModelData.selectedItem = null;
	deviceViewModelData.selectedType = null;
	
}



/**
 * Add methods to view model.
 */
function afterObservableify(deviceViewModel) {
	
	// selection handling methods
	
	deviceViewModel.selectItem = function(item, type) {
		console.log("selectItem(" + type + ", " + item.uid() + ")");
		deviceViewModel.selectedType(null);
		if (deviceViewModel.selectedItem()) {
			deviceViewModel.selectedItem().selected(false);
		}
		deviceViewModel.selectedItem(item);
		deviceViewModel.selectedType(type);
		deviceViewModel.selectedItem().selected(true);
	};
	deviceViewModel.clearSelection = function() {
		deviceViewModel.selectedItem(null);
		deviceViewModel.selectedType(null);
	};
	
	deviceViewModel.rpiSelected = ko.computed(function() {
		return deviceViewModel.selectedType() == 'rpi';
	}, deviceViewModel);
	deviceViewModel.sensorSelected = ko.computed(function() {
		return deviceViewModel.selectedType() == 'sensor';
	}, deviceViewModel);
	
	deviceViewModel.selectRPi = function(rpi) {
		deviceViewModel.selectItem(rpi, 'rpi');
	};
	deviceViewModel.selectSensor = function(sensor) {
		deviceViewModel.refreshSensor(sensor);
		deviceViewModel.selectItem(sensor, 'sensor');
	};
	
	deviceViewModel.refreshSensor = function(sensor) {
		ajax(readingURI(sensor.uid()), 'GET').done(function(readingData) {
			updateComplexObservable(sensor['readings'], readingData['SensorReadings']);
		});
	}
	
}



/**
 * Apply bindings.
 */
ajax(rpisURI, 'GET').done(function(deviceViewModelData) {
	//var deviceViewModel = {};
	
	for (var i = 0; i < deviceViewModelData['RPis'].length; ++i) {
		var rpi = deviceViewModelData['RPis'][i];
		ajaxSync(sensorURI(rpi.uid), 'GET').done(function(sensorData) {
			rpi['sensors'] = sensorData['Sensors'];
		});
	}
	
	beforeObservableify(deviceViewModelData);
	
	deviceViewModel = observableify(deviceViewModelData);
	afterObservableify(deviceViewModel);
	
	ko.applyBindings(deviceViewModel, $('#deviceView')[0]);
});