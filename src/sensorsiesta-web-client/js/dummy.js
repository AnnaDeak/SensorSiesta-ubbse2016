var runnerURI = location.origin + '/emcRunner';
var runnerViewModel = {};


/**
 * Before encoding data in observableify,
 * we need to add a few internal things: selected flags.
 */
function beforeObservableify(runnerViewModelData) {
	addSelectedKeys(runnerViewModelData);
	runnerViewModelData.selectedItem = null;
	runnerViewModelData.selectedType = null;
}



/**
 * Add methods to view model.
 */
function afterObservableify(runnerViewModel) {
	
	/**
	 * Handle selection
	 */
	runnerViewModel.selectItem = function(item, type) {
		console.log("selectItem(" + type + ", " + item.uid() + ")");
		runnerViewModel.selectedType(null);
		if (runnerViewModel.selectedItem()) {
			runnerViewModel.selectedItem().selected(false);
		}
		runnerViewModel.selectedItem(item);
		runnerViewModel.selectedType(type);
		runnerViewModel.selectedItem().selected(true);
	};
	runnerViewModel.clearSelection = function() {
		runnerViewModel.selectedItem(null);
		runnerViewModel.selectedType(null);
	};
	runnerViewModel.selectConfig = function(configuration) {
		runnerViewModel.selectItem(configuration, 'config');
	};
	runnerViewModel.selectInstance = function(instance) {
		runnerViewModel.selectItem(instance, 'instance');
	};
	runnerViewModel.selectNode = function(node) {
		runnerViewModel.selectItem(node, 'node');
	};
	runnerViewModel.nodeSelected = ko.computed(function() {
		return runnerViewModel.selectedType() == 'node';
	}, runnerViewModel);
	runnerViewModel.instanceSelected = ko.computed(function() {
		return runnerViewModel.selectedType() == 'instance';
	}, runnerViewModel);
	runnerViewModel.configSelected = ko.computed(function() {
		return runnerViewModel.selectedType() == 'config';
	}, runnerViewModel);
	
	
	/**
	 * Button handler functions for configs.
	 */
	runnerViewModel.addConfig = function() {
		console.log("addConfig()");
		var newConfig = { name: "New configuration" };
		ajax(configurationsURI, 'POST', newConfig).done(function(data) {
			runnerViewModel.configurations.push({
				uri:     ko.observable(data.configuration.uri),
				uid:     ko.observable(data.configuration.uid),
				name:    ko.observable(data.configuration.name),
				popSize: ko.observable(data.configuration.popSize),
				selected:ko.observable(false)
			});
		});
	};
	runnerViewModel.saveConfig = function(configuration) {
		console.log("saveConfig(" + configuration.uid() + ")");
		minimizedConfig = { name: configuration.name(), popSize: configuration.popSize() };
		ajax(configuration.uri(), 'PUT', minimizedConfig);
	};
	runnerViewModel.launchInstance = function(configuration, node) {
		console.log("launchInstance(" + configuration.uid() + ", " + node.uid() + ")");
		//var newInstance = { configUid: configuration.uid() };
		//ajax(instancesURI, 'POST', newInstance).done(refresh);
	};
	runnerViewModel.deleteConfig = function(configuration) {
		console.log("deleteConfig(" + configuration.uid() + ")");
		ajax(configuration.uri(), 'DELETE').done(function() {
			refresh();
			runnerViewModel.selectedItem(null);
			runnerViewModel.selectedType(null);
		});
	};
	
	
	/**
	 * Button handler functions for nodes.
	 */
	runnerViewModel.addNode = function() {
		console.log("addNode()");
	};
	runnerViewModel.saveNode = function(node) {
		console.log("saveNode(" + node.uid() + ")");
	};
	runnerViewModel.connectToNode = function(node) {
		console.log("connectToNode(" + node.uid() + ")");
		ajax(node.uri() + ".connect", 'POST').done(function(response) {
			if (response) {
				node.connected = true;
			}
		});
	};
	runnerViewModel.disconnectFromNode = function(node) {
		console.log("disconnectFromNode(" + node.uid() + ")");
	};
	
	
	
	/**
	 * Button handler functions for instances.
	 */
	runnerViewModel.resumeInstance = function(instance) {
		console.log("resumeInstance(" + instance.uid() + ")");
		if (!instance.running()) {
			ajax(instance.uri(), 'PUT', {running: true}).done(function(res) {
				instance.running(true);
			});
		}
	};
	runnerViewModel.pauseInstance = function(instance) {
		console.log("pauseInstance(" + instance.uid() + ")");
		if (instance.running()) {
			ajax(instance.uri(), 'PUT', {running: false}).done(function(res) {
				instance.running(false);
			});
		}
	};
	runnerViewModel.startInstance = function(instance) {
		console.log("startInstance(" + instance.uid() + ")");
	};
	runnerViewModel.stopInstance = function(instance) {
		console.log("stopInstance(" + instance.uid() + ")");
	};
	runnerViewModel.deleteInstance = function(instance) {
		console.log("deleteInstance(" + instance.uid() + ")");
		ajax(instance.uri(), 'DELETE').done(function() {
			refresh();
			clearSelection();
		});
	};
}



/**
 * Apply bindings.
 */
ajax(runnerURI, 'GET').done(function(runnerViewModelData) {
	var runnerViewModel = {};
	
	//beforeObservableify(dummyViewModelData);
	//runnerViewModel = observableify(dummyViewModelData);
	beforeObservableify(runnerViewModelData);
	runnerViewModel = observableify(runnerViewModelData);
	afterObservableify(runnerViewModel);
	
	ko.applyBindings(runnerViewModel, $('#runnerView')[0]);
});