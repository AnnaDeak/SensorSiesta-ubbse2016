/**
 * Standard AJAX call.
 */
function ajax(uri, method, data) {
	console.log('Sending ' + method + ' to ' + uri + ' with data: ' + ko.toJSON(data));
    var request = {
        url: uri,
        type: method,
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
        dataType: 'json',
        data: ko.toJSON(data),
        error: function(handler) {
        	if (handler.responseJSON) {
        		alert("Error " + handler.status + ": " + handler.responseJSON.msg);
        	} else {
        		alert("Error " + handler.status + ": " + handler.response);
        	}
        }
    };
    return $.ajax(request);
}

function ajaxSync(uri, method, data) {
	console.log('Sending ' + method + ' to ' + uri + ' with data: ' + ko.toJSON(data));
    var request = {
        url: uri,
        type: method,
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
        dataType: 'json',
        data: ko.toJSON(data),
        error: function(handler) {
        	if (handler.responseJSON) {
        		alert("Error " + handler.status + ": " + handler.responseJSON.msg);
        	} else {
        		alert("Error " + handler.status + ": " + handler.response);
        	}
        },
        async: false
    };
    return $.ajax(request);
}


/**
 * extra binding for knockout, to iterate through objects, not just lists.
 */
ko.bindingHandlers.foreachprop = {
	transformObject : function(obj) {
		var properties = [];
		ko.utils.objectForEach(obj, function(key, value) {
			if (!isNaN(parseInt(key))) {
				properties.push({
					key : key,
					value : value
				});
			}
		});
		return properties;
	},
	init : function(element, valueAccessor, allBindingsAccessor, viewModel,
			bindingContext) {
		var properties = ko.pureComputed(function() {
			var obj = ko.utils.unwrapObservable(valueAccessor());
			return ko.bindingHandlers.foreachprop.transformObject(obj);
		});
		ko.applyBindingsToNode(element, {
			foreach : properties
		}, bindingContext);
		return {
			controlsDescendantBindings : true
		};
	}
};

ko.bindingHandlers.foreachvalue = {
	transformObject : function(obj) {
		var properties = [];
		ko.utils.objectForEach(obj, function(key, value) {
			if (!isNaN(parseInt(key))) {
				properties.push(value);
			}
		});
		return properties;
	},
	init : function(element, valueAccessor, allBindingsAccessor, viewModel,
			bindingContext) {
		var properties = ko.pureComputed(function() {
			var obj = ko.utils.unwrapObservable(valueAccessor());
			return ko.bindingHandlers.foreachvalue.transformObject(obj);
		});
		ko.applyBindingsToNode(element, {
			foreach : properties
		}, bindingContext);
		return {
			controlsDescendantBindings : true
		};
	}
};


/**
 * Inverse bindings for enable/visible.
 */
ko.bindingHandlers.hidden = {
	update: function(element, valueAccessor) {
		var value = ko.utils.unwrapObservable(valueAccessor());
		ko.bindingHandlers.visible.update(element, function() { return !value; });
	}
};


/**
 * Bindings for ifempty, ifnotempty.
 */
ko.bindingHandlers.ifempty = {
	update: function(element, valueAccessor) {
		var value = ko.utils.unwrapObservable(valueAccessor());
		ko.bindingHandlers.visible.update(element, function() { return value.length == 0; });
	}
};
ko.bindingHandlers.ifnotempty = {
	update: function(element, valueAccessor) {
		var value = ko.utils.unwrapObservable(valueAccessor());
		ko.bindingHandlers.visible.update(element, function() { return value.length > 0; });
	}
};


/**
 * Binding to format text as date
 */
ko.bindingHandlers.dateText = {
	update : function(element, valueAccessor) {
		var value = ko.utils.unwrapObservable(valueAccessor());
		ko.bindingHandlers.text.update(element, function() {
			return new Date(value * 1000).toLocaleFormat('%Y-%m-%d %H:%M:%S');
		});
	}
};


/**
 * Add methods for evaluating whether a property has changed since loaded from
 * server.
 */
ko.observableChanging = function(value) {
	ret = ko.observable(value);
	ret._initialValue = ko.observable(value);
	ret.hasChanged = ko.computed(function() {
		return this._initialValue() != this();
	}, ret);
	return ret;
};


/**
 * Add method to an object to see which of its properties
 * have changed since loaded from server.
 */
ko.addChanged = function(obj) {
	obj.changedElements = ko.pureComputed(function() {
		var ret = {};
		for (var key in obj) {
			if (obj[key].hasChanged && obj[key].hasChanged()) {
				ret[key] = obj[key];
			}
		}
		return ret;
	}, obj);
	obj.changed = ko.pureComputed(function() {
		for (var key in obj) {
			if (obj[key].hasChanged && obj[key].hasChanged()) {
				return true;
			}
		}
		return false;
	}, obj);
};


/**
 * Add CUD operations to observed elements
 */
ko.addSave = function(obj) {
	obj.save = function() {
		ajax(obj.uri(), 'PUT', obj.changedElements()).done(function(result) {
			updateComplexObservable(obj, result);
		});
	};
};

ko.addDelete = function(obj, parent) {
	obj.del = function() {
		ajax(obj.uri(), 'DELETE').done(function() {
			parent.remove(obj);
		});
	};
};

ko.addCreate = function(obj, uri) {
	obj.create = function() {
		ajax(uri, 'POST').done(function(result) {
			newItem = observableify(result);
			newItem.del = function() {
				obj.delitem(this);
			};
			obj.push(newItem);
		});
	};
};


/**
 * Adds 'selected=false' key to all indexed elements in an object.
 */
function addSelectedKeys(obj) {
	if (obj instanceof Object) {
		// iterate through keys
		for (var key in obj) {
			// if it is a numeric string (JSON only accepts that)
			if (!isNaN(parseInt(key))) {
				// then add selected key
				obj[key].selected = false;
			}
			addSelectedKeys(obj[key]);
		}
	}
}


/**
 * Index of element in list with given UID.
 */
function indexOf(obj, uid) {
	for (var i = 0; i < obj.length; ++i) {
		if (obj[i].uid() == uid) {
			return i;
		}
	}
	return -1;
}

/**
 * Create observable values for all values in a complex object.
 * Recursively builds them with observable props.
 */
function observableify(obj, parent, key) {
	var ret;
	
	if (obj instanceof Array) {
		// arrays
		ret = ko.observableArray();
		for (var i = 0; i < obj.length; i++) {
		    ret.push(observableify(obj[i], ret, i));
		}
		if (key + '_uri' in parent) {
			arrayUri = parent[key + '_uri']();
			ko.addCreate(ret, arrayUri);
		}
	} else if (obj instanceof Object) {
		// objects
		ret = {};
		ko.addChanged(ret);
		for (var subKey in obj) {
			if (subKey.endsWith('_uri')) {
				ret[subKey] = observableify(obj[subKey], ret, subKey);
			}
		}
		for (subKey in obj) {
			if (!subKey.endsWith('_uri')) {
				ret[subKey] = observableify(obj[subKey], ret, subKey);
			}
		}
		ko.addSave(ret);
		ko.addDelete(ret, parent);
	} else {
		// just standard props
		ret = ko.observableChanging(obj);
	}
	
	return ret;
}


/**
 * Update elements of complex observable
 */
function updateComplexObservable(obj, data) {
	if (data instanceof Array) {
		for (var i = 0; i < data.length; ++i) {
			var objIdx = indexOf(obj, data[i].uid);
			if (objIdx != -1) {
				updateComplexObservable(obj[objIdx], data[i]);
			} else {
				obj.push(observableify(data[i]));
			}
		}
	} else if (data instanceof Object) {
		for (var key in data) {
			if (key in obj) {
				updateComplexObservable(obj[key], data[key]);
			} else {
				obj[key] = observableify(data[key]);
			}
		}
	} else {
		obj(data);
		if (obj._initialValue) {
			obj._initialValue(data);
		}
	}
}