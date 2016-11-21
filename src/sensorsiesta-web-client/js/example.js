var exampleURI = location.origin + '/ExampleEntitys';
var exampleViewModel = {};


/**
 * Add internal configs before observableifying data.
 */
function beforeObservableify(exampleViewModelData) {
}



/**
 * Add methods to view model.
 */
function afterObservableify(exampleViewModel) {
}



/**
 * Apply bindings.
 */
ajax(exampleURI, 'GET').done(function(exampleViewModelData) {
	var exampleViewModel = {};
	
	beforeObservableify(exampleViewModelData);
	exampleViewModel = observableify(exampleViewModelData);
	afterObservableify(exampleViewModel);
	
	ko.applyBindings(exampleViewModel, $('#exampleView')[0]);
});