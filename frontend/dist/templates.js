angular.module('datawire.templates', ['templates/directives/pager.html', 'templates/entities/icon.html', 'templates/entities/link.html', 'templates/users/profile.html', 'templates/watchlists/delete.html', 'templates/watchlists/edit.html', 'templates/watchlists/entities.html', 'templates/watchlists/frame.html', 'templates/watchlists/index.html', 'templates/watchlists/new.html']);

angular.module("templates/directives/pager.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/directives/pager.html",
    "<ul ng-show=\"showPager\" class=\"pagination pagination-sm pagination-cursors\">\n" +
    "  <li ng-class=\"{'disabled': response.prev_url==null}\"><a ng-click=\"load({url: response.prev_url})\">&laquo;</a></li>\n" +
    "  <li ng-repeat=\"page in pages\" ng-class=\"{'active': page.current}\">\n" +
    "    <a ng-click=\"load({url: page.url})\">{{page.page}}</a>\n" +
    "  </li>\n" +
    "  <li ng-class=\"{'disabled': response.next_url==null}\"><a ng-click=\"load({url: response.next_url})\">&raquo;</a></li>\n" +
    "</ul>\n" +
    "");
}]);

angular.module("templates/entities/icon.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/entities/icon.html",
    "<span class=\"entity-icon {{category}}\" tooltip=\"{{category}}\"\n" +
    "  tooltip-append-to-body=\"true\" tooltip-placement=\"left\">\n" +
    "  <i class=\"fa fa-question-circle\" ng-show=\"category=='Other'\"></i>\n" +
    "  <i class=\"fa fa-suitcase\" ng-show=\"category=='Company'\"></i>\n" +
    "  <i class=\"fa fa-university\" ng-show=\"category=='Organization'\"></i>\n" +
    "  <i class=\"fa fa-user\" ng-show=\"category=='Person'\"></i>\n" +
    "</span>\n" +
    "");
}]);

angular.module("templates/entities/link.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/entities/link.html",
    "<a>\n" +
    "  <entity-icon category=\"match.label.category\"></entity-icon>\n" +
    "  {{match.label.label}}\n" +
    "</a>\n" +
    "");
}]);

angular.module("templates/users/profile.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/users/profile.html",
    "<div class=\"modal-header\">\n" +
    "  <button type=\"button\" class=\"close\" ng-click=\"cancel()\" aria-hidden=\"true\">&times;</button>\n" +
    "  <h4 class=\"modal-title\">Profile: {{session.user.login}}</h4>\n" +
    "</div>\n" +
    "\n" +
    "<form class=\"form-horizontal\" role=\"form\" name=\"editUser\" ng-submit=\"update(editUser)\">\n" +
    "  <div class=\"modal-body\">\n" +
    "    <div class=\"form-group\" ng-class=\"{'has-error': editUser.email.$invalid}\">\n" +
    "      <label class=\"col-sm-2 control-label\" for=\"email\">E-Mail</label>\n" +
    "      <div class=\"col-sm-10\">\n" +
    "        <input type=\"text\" class=\"form-control\" id=\"email\" name=\"email\" ng-model=\"user.email\"\n" +
    "          placeholder=\"Your E-Mail\">\n" +
    "        <p class=\"help-block\" ng-show=\"editUser.email.$invalid\" ng-bind=\"editUser.email.$message\"></p>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "\n" +
    "    <div class=\"form-group\">\n" +
    "      <label class=\"col-sm-2 control-label\" for=\"api_key\">API Key</label>\n" +
    "      <div class=\"col-sm-10\">\n" +
    "        <input type=\"text\" class=\"form-control\" id=\"api_key\" name=\"api_key\" ng-model=\"session.api_key\"\n" +
    "          disabled>\n" +
    "        <span class=\"help-block\">Use the API key to read and write data via a remote application or client library.</span>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"modal-footer\">\n" +
    "    <button type=\"button\" class=\"btn btn-default\" ng-click=\"cancel()\">Cancel</button>\n" +
    "    <button type=\"submit\" class=\"btn btn-primary\">Save</button>\n" +
    "  </div>\n" +
    "</form>\n" +
    "");
}]);

angular.module("templates/watchlists/delete.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/watchlists/delete.html",
    "<div class=\"modal-header\">\n" +
    "  <button type=\"button\" class=\"close\" ng-click=\"cancel()\" aria-hidden=\"true\">&times;</button>\n" +
    "  <h4 class=\"modal-title\">Delete: {{list.label}}</h4>\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"modal-body\">\n" +
    "  <p>Deleting the list <strong>{{list.label}}</strong> will also delete\n" +
    "  all entities associated with this list. Are you sure?</p>\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"modal-footer\">\n" +
    "  <button type=\"button\" class=\"btn btn-default\" ng-click=\"cancel()\">Cancel</button>\n" +
    "  <button type=\"submit\" class=\"btn btn-danger\" ng-click=\"delete()\">Delete</button>\n" +
    "</div>\n" +
    "");
}]);

angular.module("templates/watchlists/edit.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/watchlists/edit.html",
    "<lists-frame list=\"list\" selected=\"edit\">\n" +
    "  <form class=\"form-horizontal\" role=\"form\" name=\"editList\" ng-submit=\"save(editList)\">\n" +
    "    <div class=\"row\">\n" +
    "      <div class=\"col-md-6\">   \n" +
    "        <div class=\"form-group\" ng-class=\"{'has-error': editList.label.$invalid}\">\n" +
    "          <label class=\"col-sm-3 control-label\" for=\"label\">Label</label>\n" +
    "          <div class=\"col-sm-9\">\n" +
    "            <input type=\"text\" class=\"form-control\" id=\"label\" name=\"label\" ng-model=\"list.label\"\n" +
    "              placeholder=\"The list's label\">\n" +
    "            <p class=\"help-block\" ng-show=\"editList.label.$invalid\" ng-bind=\"editList.label.$message\"></p>\n" +
    "          </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"form-group\">\n" +
    "          <div class=\"col-sm-offset-3 col-sm-9\">\n" +
    "            <div class=\"checkbox\">\n" +
    "              <label>\n" +
    "                <input type=\"checkbox\" ng-model=\"list.public\"> Publicly visible\n" +
    "              </label>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"form-group\">\n" +
    "          <div class=\"col-sm-offset-3 col-sm-9\">\n" +
    "            <button type=\"submit\" class=\"btn btn-primary\"\n" +
    "              ng-disabled=\"!canSave()\">Save</button>\n" +
    "            <button type=\"button\" ng-click=\"delete()\" class=\"btn btn-danger\">Delete</button>\n" +
    "          </div>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "\n" +
    "\n" +
    "      <div class=\"col-md-6\">\n" +
    "        <table class=\"table table-condensed\">\n" +
    "          <tr>\n" +
    "            <th colspan=\"2\">Users who have access</th>\n" +
    "          </tr>\n" +
    "          <tr ng-repeat=\"user in users.results\">\n" +
    "            <td width='1%'>\n" +
    "              <input type=\"checkbox\" ng-checked=\"hasUser(user.id)\"\n" +
    "                ng-click=\"toggleUser(user.id)\">\n" +
    "            </td>\n" +
    "            <td>{{user.display_name}}</td>\n" +
    "          </tr>\n" +
    "        </table>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "  </form>\n" +
    "</lists-frame>\n" +
    "");
}]);

angular.module("templates/watchlists/entities.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/watchlists/entities.html",
    "<lists-frame list=\"list\" selected=\"entities\">\n" +
    "  <form class=\"search-bar\" ng-submit=\"filter()\">\n" +
    "    <div class=\"row\">\n" +
    "      <div class=\"col-md-12\">\n" +
    "        <div class=\"input-group\">\n" +
    "          <div class=\"input-group-addon\">\n" +
    "            <i class=\"fa fa-search\"></i>\n" +
    "          </div>\n" +
    "          <input type=\"text\" class=\"form-control\" id=\"prefix-search\"\n" +
    "            ng-model=\"query.prefix\"\n" +
    "            placeholder=\"Filter by name\">\n" +
    "          <span class=\"input-group-btn\">\n" +
    "            <button class=\"btn btn-success\" type=\"button\" ng-click=\"setEdit('new')\">\n" +
    "              <i class=\"fa fa-plus-square\"></i> New\n" +
    "            </button>\n" +
    "          </span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "  </form>\n" +
    "\n" +
    "\n" +
    "  <table class=\"table table-striped\">\n" +
    "    <!--tr>\n" +
    "      <th colspan=\"2\">Name</th>\n" +
    "      <th>Aliases</th>\n" +
    "      <th width=\"10%\"></th>\n" +
    "    </tr-->\n" +
    "    <tr>\n" +
    "      <td colspan=\"4\" ng-show=\"edit == 'new'\">\n" +
    "        <div class=\"alert alert-info\" ng-show=\"entities.total == 0 && query.prefix.length\">\n" +
    "          <strong>No matches were found.</strong> Why don't you create a new entity to track \n" +
    "          this company or person?\n" +
    "        </div>\n" +
    "        <form class=\"form-horizontal\" name=\"newEntityForm\" ng-submit=\"create(newEntityForm)\">\n" +
    "          <div class=\"form-group\">\n" +
    "            <label for=\"label\" class=\"col-sm-2 control-label\">Label</label>\n" +
    "            <div class=\"col-sm-10\">\n" +
    "              <input type=\"label\" class=\"form-control\" id=\"edit-label-new\"\n" +
    "                 ng-model=\"newEntity.label\"\n" +
    "                placeholder=\"Name\">\n" +
    "              <p class=\"help-block\" ng-show=\"newEntityForm.label.$invalid\" ng-bind=\"newEntityForm.label.$message\"></p>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "          <div class=\"form-group\">\n" +
    "            <label for=\"aliases\" class=\"col-sm-2 control-label\">a.k.a.</label>\n" +
    "            <div class=\"col-sm-10\">\n" +
    "              <input type=\"label\" class=\"form-control\" id=\"aliases\" ng-model=\"newEntity.aliases\"\n" +
    "                placeholder=\"Known aliases and alternate spellings of the name, separated by commas.\">\n" +
    "            </div>\n" +
    "          </div>\n" +
    "          <div class=\"form-group\">\n" +
    "            <div class=\"col-sm-offset-2 col-sm-2\">\n" +
    "              <div class=\"radio\">\n" +
    "                <label>\n" +
    "                  <input type=\"radio\" ng-model=\"newEntity.category\" value=\"Person\"> Person\n" +
    "                </label>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-sm-2\">\n" +
    "              <div class=\"radio\">\n" +
    "                <label>\n" +
    "                  <input type=\"radio\" ng-model=\"newEntity.category\" value=\"Company\"> Company\n" +
    "                </label>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-sm-2\">\n" +
    "              <div class=\"radio\">\n" +
    "                <label>\n" +
    "                  <input type=\"radio\" ng-model=\"newEntity.category\" value=\"Organization\"> Organization\n" +
    "                </label>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-sm-2\">\n" +
    "              <div class=\"radio\">\n" +
    "                <label>\n" +
    "                  <input type=\"radio\" ng-model=\"newEntity.category\" value=\"Other\"> Other\n" +
    "                </label>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "          <div class=\"form-group\">\n" +
    "            <div class=\"col-sm-offset-2 col-sm-10\">\n" +
    "              <button type=\"submit\" class=\"btn btn-success\">\n" +
    "                Create\n" +
    "              </button>\n" +
    "              <button type=\"button\" class=\"btn btn-default\" ng-click=\"setEdit(null)\">\n" +
    "                Cancel\n" +
    "              </button>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "        </form>\n" +
    "      </td>\n" +
    "    </tr>\n" +
    "    <tr ng-repeat-start=\"entity in entities.results\" ng-hide=\"edit == entity.id\">\n" +
    "      <td width=\"1%\">\n" +
    "        <entity-icon category=\"entity.category\"></entity-icon>\n" +
    "      </td>\n" +
    "      <td width=\"30%\">\n" +
    "        {{ entity.label }}\n" +
    "      </td>\n" +
    "      <td>\n" +
    "        {{ entity.aliases }}\n" +
    "      </td>\n" +
    "      <td width=\"10%\" class=\"actions\">\n" +
    "        <div class=\"btn-group btn-group-sm\" role=\"group\">\n" +
    "          <button type=\"button\" class=\"btn btn-default\" ng-click=\"setEdit(entity.id)\">\n" +
    "            <i class=\"fa fa-pencil-square-o\"></i>\n" +
    "          </button>\n" +
    "          <button type=\"button\" class=\"btn btn-danger\" ng-click=\"delete(entity)\">\n" +
    "            <i class=\"fa fa-trash\"></i>\n" +
    "          </button>\n" +
    "        </div>\n" +
    "      </td>\n" +
    "    </tr>\n" +
    "    <tr ng-repeat-end>\n" +
    "      <td colspan=\"4\" ng-show=\"edit == entity.id\">\n" +
    "        <form class=\"form-horizontal\" name=\"editEntity\" ng-submit=\"update(editEntity, entity)\">\n" +
    "          <div class=\"form-group\">\n" +
    "            <label for=\"label\" class=\"col-sm-2 control-label\">Label</label>\n" +
    "            <div class=\"col-sm-10\">\n" +
    "              <input type=\"label\" class=\"form-control\" id=\"edit-label-{{entity.id}}\"\n" +
    "                 ng-model=\"entity.label\"\n" +
    "                placeholder=\"Name\">\n" +
    "              <p class=\"help-block\" ng-show=\"editEntity.label.$invalid\" ng-bind=\"editEntity.label.$message\"></p>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "          <div class=\"form-group\">\n" +
    "            <label for=\"aliases\" class=\"col-sm-2 control-label\">a.k.a.</label>\n" +
    "            <div class=\"col-sm-10\">\n" +
    "              <input type=\"label\" class=\"form-control\" id=\"aliases\" ng-model=\"entity.aliases\"\n" +
    "                placeholder=\"Known aliases and alternate spellings of the name, separated by commas.\">\n" +
    "            </div>\n" +
    "          </div>\n" +
    "          <div class=\"form-group\">\n" +
    "            <div class=\"col-sm-offset-2 col-sm-2\">\n" +
    "              <div class=\"radio\">\n" +
    "                <label>\n" +
    "                  <input type=\"radio\" ng-model=\"entity.category\" value=\"Person\"> Person\n" +
    "                </label>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-sm-2\">\n" +
    "              <div class=\"radio\">\n" +
    "                <label>\n" +
    "                  <input type=\"radio\" ng-model=\"entity.category\" value=\"Company\"> Company\n" +
    "                </label>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-sm-2\">\n" +
    "              <div class=\"radio\">\n" +
    "                <label>\n" +
    "                  <input type=\"radio\" ng-model=\"entity.category\" value=\"Organization\"> Organization\n" +
    "                </label>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-sm-2\">\n" +
    "              <div class=\"radio\">\n" +
    "                <label>\n" +
    "                  <input type=\"radio\" ng-model=\"entity.category\" value=\"Other\"> Other\n" +
    "                </label>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "          <div class=\"form-group\">\n" +
    "            <div class=\"col-sm-offset-2 col-sm-10\">\n" +
    "              <button type=\"submit\" class=\"btn btn-success\">\n" +
    "                Save\n" +
    "              </button>\n" +
    "              <button type=\"button\" class=\"btn btn-default\" ng-click=\"setEdit(null)\">\n" +
    "                Cancel\n" +
    "              </button>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "        </form>\n" +
    "      </td>\n" +
    "    </tr>\n" +
    "  </table>\n" +
    "  <aleph-pager class=\"pull-right\" response=\"entities\" load=\"loadUrl(url)\"></aleph-pager>\n" +
    "</lists-frame>\n" +
    "");
}]);

angular.module("templates/watchlists/frame.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/watchlists/frame.html",
    "<ol class=\"breadcrumb\">\n" +
    "  <li>\n" +
    "    <a href=\"/\">Home</a>\n" +
    "  </li>\n" +
    "  <li>\n" +
    "    Lists of people and companies\n" +
    "  </li>\n" +
    "  <li ng-show=\"list\" class=\"active\">\n" +
    "    {{list.label}}\n" +
    "  </li>\n" +
    "</ol>\n" +
    "\n" +
    "<div class=\"row\">\n" +
    "  <div class=\"col-md-3\">\n" +
    "    <ul class=\"nav nav-pills nav-stacked\">\n" +
    "      <li ng-repeat=\"lst in lists.results\"\n" +
    "          ng-class=\"{'active': list.id == lst.id}\">\n" +
    "        <a href=\"/lists/{{lst.id}}/entities\">\n" +
    "          <i class=\"fa fa-list\"></i> {{lst.label}}\n" +
    "        </a>\n" +
    "      </li>\n" +
    "      <li ng-class=\"{'active': list.new}\">\n" +
    "        <a href=\"/lists/new\">\n" +
    "          <i class=\"fa fa-plus-square\"></i> Create a new list\n" +
    "        </a>\n" +
    "      </li>\n" +
    "    </ul>\n" +
    "  </div>\n" +
    "  <div class=\"col-md-9\">\n" +
    "    <ul class=\"nav nav-tabs\" ng-show=\"selected\">\n" +
    "      <li role=\"presentation\" ng-class=\"{'active': selected == 'entities'}\">\n" +
    "        <a href=\"/lists/{{list.id}}/entities\">Manage people and companies</a>\n" +
    "      </li>\n" +
    "      <li role=\"presentation\" ng-class=\"{'active': selected == 'edit'}\">\n" +
    "        <a href=\"/lists/{{list.id}}\">List settings</a>\n" +
    "      </li>\n" +
    "    </ul>\n" +
    "    <div ng-transclude></div>\n" +
    "  </div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("templates/watchlists/index.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/watchlists/index.html",
    "huhu\n" +
    "");
}]);

angular.module("templates/watchlists/new.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/watchlists/new.html",
    "<lists-frame list=\"list\">\n" +
    "  <form class=\"form-horizontal\" role=\"form\" name=\"newList\" ng-submit=\"create(newList)\">\n" +
    "    <div class=\"row\">\n" +
    "      <div class=\"col-md-6\">   \n" +
    "        <div class=\"form-group\" ng-class=\"{'has-error': newList.label.$invalid}\">\n" +
    "          <label class=\"col-sm-3 control-label\" for=\"label\">Label</label>\n" +
    "          <div class=\"col-sm-9\">\n" +
    "            <input type=\"text\" class=\"form-control\" id=\"label\" name=\"label\" ng-model=\"list.label\"\n" +
    "              placeholder=\"The list's label\">\n" +
    "            <p class=\"help-block\" ng-show=\"newList.label.$invalid\" ng-bind=\"newList.label.$message\"></p>\n" +
    "          </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"form-group\">\n" +
    "          <div class=\"col-sm-offset-3 col-sm-9\">\n" +
    "            <div class=\"checkbox\">\n" +
    "              <label>\n" +
    "                <input type=\"checkbox\" ng-model=\"list.public\"> Publicly visible\n" +
    "              </label>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"form-group\">\n" +
    "          <div class=\"col-sm-offset-3 col-sm-9\">\n" +
    "            <button type=\"submit\" class=\"btn btn-primary\"\n" +
    "              ng-disabled=\"!canCreate()\">Create</button>\n" +
    "          </div>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "  </form>\n" +
    "</lists-frame>\n" +
    "");
}]);
