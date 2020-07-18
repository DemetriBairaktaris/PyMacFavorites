import Foundation
import uuid
import os

path_to_favorites = "/Users/{user}/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.FavoriteItems.sfl2"


def _get_url_from_item(item):
    url, _, _ = Foundation.NSURL.initByResolvingBookmarkData_options_relativeToURL_bookmarkDataIsStale_error_(
        Foundation.NSURL.alloc(),
        item["Bookmark"],
        Foundation.NSURLBookmarkResolutionWithoutUI,
        None,
        None,
        None,
    )

    return url


def _get_existing_urls(user):
    data = Foundation.NSKeyedUnarchiver.unarchiveObjectWithFile_(path_to_favorites.format(user=user))
    urls = []
    if data is not None:
        data_items = data.get("items", [])
        for item in data_items:
            i = _get_url_from_item(item)
            if i is None:
                continue
            urls.append(_get_url_from_item(item))
    return urls


def _add_scheme_if_none(path):
    if not path.startswith("file://"):
        return "file://" + path


def update_favorites(user, add_items, remove_items):
    "Set the Server Favorites for the given user"

    # read existing favorites file
    data = Foundation.NSKeyedUnarchiver.unarchiveObjectWithFile_(path_to_favorites.format(user=user))

    new_add_items = []
    for s in add_items:
        new_add_items.append((s, s))

    add_items = new_add_items
    existing_items = []

    # read existing items
    if data is not None:
        data_items = data.get("items", [])
        # read existing servers
        for item in data_items:
            # name = item["Name"]
            item = Foundation.NSDictionary.dictionaryWithDictionary_(item)
            url, _, _ = Foundation.NSURL.initByResolvingBookmarkData_options_relativeToURL_bookmarkDataIsStale_error_(
                Foundation.NSURL.alloc(),
                item["Bookmark"],
                Foundation.NSURLBookmarkResolutionWithoutUI,
                None,
                None,
                None,
            )
            unicode_url = url.path()
            if unicode_url != "None":
                existing_items.append((unicode_url, item))

    # get unique ordered list of all items
    all_items = []
    # add existing_items to list, updating name if necessary
    for s in existing_items:
        try:
            idx = [a[1] for a in add_items].index(s[1])
            all_items.append((add_items[idx][0], s[1]))
        except ValueError:
            all_items.append(s)
    # Add items from 'add_items' array
    for s in add_items:
        if s[0] not in [e[0] for e in existing_items]:
            item = {}
            # use unicode to translate to NSString
            url = Foundation.NSURL.URLWithString_((s[0]))
            bookmark, _ = url.bookmarkDataWithOptions_includingResourceValuesForKeys_relativeToURL_error_(0, None, None,
                                                                                                          None)
            item["Bookmark"] = bookmark
            # generate a new UUID for each server
            item["uuid"] = str(uuid.uuid1()).upper()
            item["visibility"] = 0
            item["CustomItemProperties"] = Foundation.NSDictionary.new()
            item_to_append = Foundation.NSDictionary.dictionaryWithDictionary_(item)
            all_items.append(((s[0]), item_to_append))

    # Remove items from 'remove_items' array


    all_items = [s for s in all_items if s[0] not in remove_items]


    # Set items:
    items = [s[1] for s in all_items]
    data = Foundation.NSDictionary.dictionaryWithDictionary_({
        "items": Foundation.NSArray.arrayWithArray_(items),
        "properties": Foundation.NSDictionary.dictionaryWithDictionary_(
            {"com.apple.LSSharedFileList.ForceTemplateIcons": False})
    })

    # Write sfl2 file
    Foundation.NSKeyedArchiver.archiveRootObject_toFile_(data, path_to_favorites.format(user=user))


def get_favorites(user) -> list:
    existing_items = []
    for url in _get_existing_urls(user):
        native_os_path = str(url.path())
        if native_os_path and native_os_path != "None":
            existing_items.append(native_os_path)
    return existing_items


def refresh():
    os.system("killall sharedfilelistd")
    os.system("killall Finder")

