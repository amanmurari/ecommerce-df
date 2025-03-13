import ClassicEditor from './src/ckeditor';
import './src/override-django.css';
//import ImageLoadObserver from '@ckeditor/ckeditor5-image/src/image/imageloadobserver';
let editors = [];

/**
 * Creates a custom event named 'djcke.djCkeEditorCleanUp' and makes it globally available on the `window` object.
 * 
 * This event is intended to be dispatched when images are removed from a CKEditor instance, 
 * allowing other parts of the application to listen for and respond to this event.
 * Use this when you are not using a form submit, eg HTMX Post to do final cleanup of the editor
 */

window.djCkeEditorCleanUp = new CustomEvent('djcke.djCkeEditorCleanUp', {
    detail: {
        sender: null
    }

});

/**
 * Custom event to enable the read-only mode for a CKEditor instance globally.
 *
 * @event djcke.djCkeEnableGlobalReadonly
 * @type {CustomEvent}
 * @property {object} detail -  Details about the read-only mode.
 * @property {boolean} detail.hideToolbar - Indicates whether to hide the 
 *                                          toolbar in read-only mode. 
 *                                          Defaults to false.
 * 
 * @example
 * // Dispatch the event to enable read-only mode and hide the toolbar
 * window.dispatchEvent(new CustomEvent('djcke.djCkeEnableGlobalReadonly', {
 *   detail: { hideToolbar: true }
 * }));
 */
window.djCkeEnableGlobalReadonly= new CustomEvent('djcke.djCkeEnableGlobalReadonly', {
    detail: {
        hideToolbar: false
    }

});

/**
 * Custom event to disable the read-only mode for a CKEditor instance globally.
 *
 * @event djcke.djCkeDisableGlobalReadonly
 * @type {CustomEvent}
 * @property {object} detail - Details about the read-only mode.
 * @property {boolean} detail.hideToolbar - Indicates whether the toolbar was 
 *                                          hidden in read-only mode. 
 *                                          Defaults to false.
 * 
 * @example
 * // Dispatch the event to disable read-only mode
 * window.dispatchEvent(new CustomEvent('djcke.djCkeDisableGlobalReadonly')); 
 */
window.djCkeDisableGlobalReadonly= new CustomEvent('djcke.djCkeDisableGlobalReadonly', {
    detail: {
        hideToolbar: false
    }

});

window.createEditors = createEditors;

function createEditors(element = document.body) {

    // Find all elements within the specified container (or entire document body)
    // that have the class 'django_ckeditors' (these are our CKEditor targets).
    const allEditors = resolveElementArray(element, '.django_ckeditors');

    allEditors.forEach(editorEl => {
        // Check if this element is part of a Django formset template or 
        // has already been processed.
        if (
            editorEl.id.indexOf('__prefix__') !== -1 ||
                editorEl.getAttribute('data-processed') === '1'
        ) {
            return
        }
        const script_id = `${editorEl.id}_script`;
        editorEl.nextSibling.remove();

        const upload_image_url = element.querySelector(
            `#${script_id}-ck-editors-upload-url`
        ).getAttribute('data-upload-image-url');

        const upload_unused_image_url = element.querySelector(
            `#${script_id}-ck-editors-upload-url`
        ).getAttribute('data-upload-unused-image-url');


        const csrf_cookie_name = element.querySelector(
            `#${script_id}-ck-editors-upload-url`
        ).getAttribute('data-csrf_cookie_name');

        const data_extra = JSON.stringify(JSON.parse(element.querySelector(
            `#${script_id}-ck-editors-upload-url`
        ).getAttribute('data-extra')));

        const labelElement = element.querySelector(`[for$="${editorEl.id}"]`);
        if (labelElement) {
            labelElement.style.float = 'none';
        }

        const config = JSON.parse(
            element.querySelector(`#${script_id}-span`).textContent,
            (key, value) => {
                var match = value.toString().match(new RegExp('^/(.*?)/([gimy]*)$'));
                if (match) {
                    var regex = new RegExp(match[1], match[2]);
                    return regex;
                }
                return value;
            }
        );
        config.simpleUpload = {
            'uploadUrl': upload_image_url, 
            'headers': {
                'X-CSRFToken': getCookie(csrf_cookie_name),
                'X-Data-Extra': data_extra,
            }
        };

        ClassicEditor.create(editorEl, config)
            .then(editor => {

                //  WordCount plugin handling
                if (editor.plugins.has('WordCount')) {
                    const wordCountPlugin = editor.plugins.get('WordCount');
                    const wordCountWrapper = element.querySelector(`#${script_id}-word-count`);
                    wordCountWrapper.innerHTML = '';
                    wordCountWrapper.appendChild(wordCountPlugin.wordCountContainer);
                };

                // Declare constants
                // Extract initial image URLs for this editor when instantiated
                // The purpose is to collect all images for existing editor edits
                const allEncounteredImageUrls=extractImageUrls(editor.getData()); 
                const currentEditorImageUrls=[];
                const form = editor.ui.view.element.closest('form');

                // Declare variables
                let editorChanged = false;
                let editorCurrentContent="";
                let isProcessing = false; // Flag to track if processing is in progress

                // This is highly inefficient.  The ImageLaadObserver
                // is not playing nicely so I will need to come back
                // and work on it when I have some time...
                editor.model.document.on('change:data', () => {
                    if (isProcessing) {
                        return; // Skip processing if already in progress
                    }

                    isProcessing = true;
                    editorChanged=true;
                    editorCurrentContent = editor.getData();
                    currentEditorImageUrls.length=0;
                    currentEditorImageUrls.push(...extractImageUrls(editorCurrentContent));
                    allEncounteredImageUrls.push(...currentEditorImageUrls);
                    removeDuplicatesInPlace(allEncounteredImageUrls);
                    // Schedule the flag reset after 1 second
                    setTimeout(() => {
                        isProcessing = false;
                    }, 100); // 100 milliseconds = 0.1 second


                });

                //form.addEventListener('submit', () => {
                //
                //    const editorIdToRemove = editor.id; 
                //    const indexToRemove = editors.findIndex(editor => editor.id === editorIdToRemove);
                //
                //    if (indexToRemove !== -1) { // Check if the editor was found
                //        editor.updateSourceElement();
                //        processRemovedImages(editor,  allEncounteredImageUrls, upload_unused_image_url, csrf_cookie_name);
                //        editors.splice(indexToRemove, 1); 
                //        editor.destroy();
                //    } else {
                //        console.warn("Submit Button: Editor with ID not found:", editorIdToRemove);
                //    }
                //});
                //

                // Declare the variable for height transition
                let originalToolbarHeight = null;

                document.addEventListener('djcke.djCkeEnableGlobalReadonly', (event) => {
                    editor.enableReadOnlyMode(editor.id);

                    const toolbarElement = editor.ui.view.toolbar.element;

                    if (event.detail.hideToolbar) {
                        originalToolbarHeight =  getComputedStyle(toolbarElement).height; // Get initial height
                        toolbarElement.style.height = originalToolbarHeight

                        // Wait for the next frame to ensure the initial height is set
                        requestAnimationFrame(() => {
                            toolbarElement.style.height = '0'; // Transition height to 0
                        });
                    } else {
                        toolbarElement.style.display = 'flex'; // Or 'block' if that's the default
                        toolbarElement.style.height = 'auto'; // Restore original height
                    }
                });

                document.addEventListener('djcke.djCkeDisableGlobalReadonly', (event) => {
                    editor.disableReadOnlyMode(editor.id);

                    const toolbarElement = editor.ui.view.toolbar.element;

                    if (originalToolbarHeight) {

                        toolbarElement.style.height = '0px';

                        // Wait for the next frame to ensure the height is applied
                        requestAnimationFrame(() => {

                            toolbarElement.style.height = originalToolbarHeight; // Transition height to the original setting

                            // Reset after the transition is complete
                            setTimeout(() => {
                                originalToolbarHeight = null;
                                toolbarElement.style.display = 'flex'; // Restore original display
                                toolbarElement.style.height = 'auto'; // Restore original height

                            }, 300); 
                        });
                    } else {
                        // If originalToolbarHeight is not available, use the fallback method
                        toolbarElement.style.display = 'flex';
                        toolbarElement.classList.add('ck-toolbar-transition');
                        toolbarElement.offsetHeight; 
                        toolbarElement.style.height = 'auto'; 
                    }
                });

                document.addEventListener('djcke.djCkeEditorCleanUp', (event) => {
                    // Call the extracted function
                    // Find the index of the editor with the matching ID
                    const editorIdToRemove = editor.id; 
                    const indexToRemove = editors.findIndex(editor => editor.id === editorIdToRemove);

                    if (indexToRemove !== -1) { // Check if the editor was found
                        editor.updateSourceElement();

                        processRemovedImages(editor,  allEncounteredImageUrls, upload_unused_image_url, csrf_cookie_name);
                        editor.destroy();
                        editors.splice(indexToRemove, 1); 
                        //console.log("Removed editor with ID:", editorIdToRemove);
                    } else {
                        console.warn("Removal Event: Editor with ID not found:", editorIdToRemove);
                    }
                    //console.log('EDITORS AFTER REMOVAL', editors);

                });

                editors.push(editor);
            }).catch(error => {
                console.error((error));
            });
        editorEl.setAttribute('data-processed', '1');
    });

    window.editors = editors;
    window.ClassicEditor = ClassicEditor;
}

/**
 * Processes removed images from a CKEditor instance, potentially sending them to the server for further handling.
 *
 * @param {Array<string>} allEncounteredImageUrls - An array of all image URLs encountered so far in the editor.
 * @param {string} finalContent - The final HTML content of the editor after potential changes.
 * @param {ClassicEditor} editor - The CKEditor instance.
 * @param {string} uploadUnusedImageUrl - The URL of the server endpoint to handle removed image URLs.
 * @param {string} csrfCookieName - The name of the CSRF cookie for security.
 * @returns {Promise} - A promise that resolves when the image removal processing is complete (with or without server interaction).
 */
function processRemovedImages(editor,  allEncounteredImageUrls, uploadUnusedImageUrl, csrfCookieName) {
    return new Promise((resolve, reject) => {
        const editorCurrentContent = editor.getData();
        // Extract image URLs from the final content
        const editorCurrentImageUrls = extractImageUrls(editorCurrentContent);

        removeDuplicatesInPlace(allEncounteredImageUrls);
        // Identify image URLs that have been removed from the editor
        const editorRemovedImageUrlsArray = handleImageRemovals(allEncounteredImageUrls, editorCurrentContent, editor);
        //console.log('PROCESSING: PROMISE INIT REMOVED IMAGES:', editorRemovedImageUrlsArray)

        resolve(editorRemovedImageUrlsArray);
    })
        .then(editorRemovedImageUrlsArray => {

            // If there are removed images, send them to the server
            if (editorRemovedImageUrlsArray.length > 0) {
                //console.log("**** SENDING REMOVED IMAGES ****", editorRemovedImageUrlsArray);
                //console.log("**** SENDING REMOVED IMAGES LENGTH ****", editorRemovedImageUrlsArray.length);

                return sendRemovedImagesArrayToServer(editorRemovedImageUrlsArray, uploadUnusedImageUrl, getCookie(csrfCookieName), editor);
            } else {
                // If no images were removed, return a resolved promise
                return Promise.resolve();
            }
        })
        .then(serverResponseData => {
            if (serverResponseData && 'success' in serverResponseData) {
                //console.log('SUCCESS: Data from server:', serverResponseData);
            } else if (serverResponseData && 'error' in serverResponseData) {
                //console.log('ERROR: Data from server:', serverResponseData);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            setTimeout(() => {
                //console.log('**** IMAGE REMOVAL TIMER  ****')
            }, 0);

        });
}

/**
 * Sends an array of removed image URLs to the server using a POST request.
 *
 * @param {Array<string>} imageUrlArray - An array of image URLs to be sent to the server.
 * @param {string} endpointUrl - The URL of the server endpoint to handle the request.
 * @param {string} csrf_cookie - The CSRF token value for security.
 * @param {ClassicEditor} editor - The CKEditor instance (optional, for debugging or context).
 * @returns {Promise} - A promise that resolves with the server's response data or rejects with an error.
 */
function sendRemovedImagesArrayToServer(imageUrlArray, endpointUrl, csrf_cookie, editor) {
    return new Promise((resolve, reject) => {

        fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_cookie,
            },
            body: JSON.stringify({ imageUrls: imageUrlArray }),
        })
            .then(response => {
                if (!response.ok) {
                    reject(new Error('Network response was not ok'));
                }
                return response.json();
            })
            .then(data => {
                resolve(data); // Resolve the promise with the server response data
            })
            .catch(error => {
                console.error('Error sending image URL:', error);
                reject(error); // Reject the promise with the error
            });
    });
}

// This just keeps the arrays sensible until
// I can get the ImageLoadObserver playing nicely...
/**
 * Removes duplicate elements from an array in-place, including handling nested arrays and empty arrays.
 *
 * @param {Array} arr - The array to de-duplicate.
 */
function removeDuplicatesInPlace(arr) {
    const seen = new Set();
    for (let i = 0; i < arr.length; i++) {
        const element = arr[i];

        // Handle nested arrays
        if (Array.isArray(element)) {
            removeDuplicatesInPlace(element); // Recursively remove duplicates within nested arrays

            // Handle empty arrays explicitly
            if (element.length === 0) {
                arr.splice(i, 1);
                i--;
                continue; // Skip to the next iteration after removing an empty array
            }

            // Convert nested array to a string for comparison in the Set
            const stringifiedElement = JSON.stringify(element);
            if (seen.has(stringifiedElement)) {
                arr.splice(i, 1);
                i--;
            } else {
                seen.add(stringifiedElement);
            }
        } else if (seen.has(element) || element === '') {
            arr.splice(i, 1);
            i--;
        } else {
            seen.add(element);
        }
    }
}

/**
 * Handles the identification and processing of removed images from a CKEditor instance.
 *
 * @param {Array<string>} allEncounteredImageUrls - An array of all image URLs encountered so far in the editor.
 * @param {string} finalContent - The final HTML content of the editor after potential changes.
 * @param {ClassicEditor} editor - The CKEditor instance (optional, for debugging or context).
 * @returns {Array<string>} - An array of image URLs that were removed from the editor's content.
 */
function handleImageRemovals(allEncounteredImageUrls, finalContent, editor) {
    try {
        // Extract image URLs from the final content
        const editorFinalImageUrls = extractImageUrls(finalContent);
        const editorRemovedImageUrlsArray = [];
        // Find removed images and add their URLs to the array
        editorRemovedImageUrlsArray.push(...findRemovedImages(allEncounteredImageUrls, editorFinalImageUrls, editor));
        return editorRemovedImageUrlsArray; 
    } catch (error) {
        // Handle potential errors during image removal processing
        console.error('Error in handleImageRemovals:', error);

        // Return an empty array to indicate no removals (or adjust as needed)
        return []; 
    }
}

/**
 * Finds and returns image URLs that were removed from the editor's content.
 *
 * @param {Array<string>} allEncounteredImageUrls - An array of all image URLs encountered so far in the editor.
 * @param {Array<string>} editorFinalImageUrls - An array of image URLs currently present in the editor's content.
 * @param {ClassicEditor} editor - The CKEditor instance (optional, for debugging or context).
 * @returns {Array<string>} - An array of image URLs that were removed from the editor's content.
 */
function findRemovedImages(allEncounteredImageUrls, editorFinalImageUrls,editor) {
    // If there are no final image URLs (e.g., the editor is empty), 
    // return all encountered image URLs as removed.
    if (!editorFinalImageUrls) {
        //console.log('editorFinalImageUrls is empty, returning all:' , allEncounteredImageUrls);
        return allEncounteredImageUrls;
    };
    // Filter allEncounteredImageUrls to keep only those not present in editorFinalImageUrls
    const filteredImageUrls = allEncounteredImageUrls.filter(imageUrl => !editorFinalImageUrls.includes(imageUrl));

    return filteredImageUrls;
}

/**
 * Retrieves the value of a cookie with the specified name.
 *
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} - The cookie's value if found, otherwise null.
 */
function getCookie(name) {
    let cookieValue = null;
    // Check if there are any cookies set
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Check if this cookie's name matches the provided name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Extract and decode the value
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Checks whether the element or its children match the query and returns
 * an array with the matches.
 * 
 * @param {!HTMLElement} element
 * @param {!string} query
 * 
 * @returns {array.<HTMLElement>}
 */
function resolveElementArray(element, query) {
    return element.matches(query) ? [element] : [...element.querySelectorAll(query)];
}


// Function to extract image URLs from CKEditor content (HTML string)
function extractImageUrls(content) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(content, 'text/html');
    const images = doc.querySelectorAll('img');

    return Array.from(images).map(img => img.src);
}


/**
 * This function filters the list of mutations only by added elements, thus
 * eliminates the occurrence of text nodes and tags where it does not make sense
 * to try to use with `QuerySelectorAll()` and `matches()` functions.
 * 
 * @param {MutationRecord} recordList - It is the object inside the array
 * passed to the callback of a MutationObserver.
 * 
 * @returns {Array} Array containing filtered nodes.
 */
function getAddedNodes(recordList) {
    return recordList
        .flatMap(({ addedNodes }) => Array.from(addedNodes))
        .filter(node => node.nodeType === 1);
}


document.addEventListener("DOMContentLoaded", () => {
    createEditors();

    if (typeof django === "object" && django.jQuery) {
        django.jQuery(document).on("formset:added", createEditors);
    }

    const observer = new MutationObserver((mutations) => {
        let addedNodes = getAddedNodes(mutations);

        addedNodes.forEach(node => {
            // Initializes editors
            createEditors(node);
        });
    });

    // Configure MutationObserver options
    const observerOptions = {
        childList: true,
        subtree: true,
    };

    // Selects the parent element where the events occur
    const mainContent = document.body;
    const modalContainer = document.getElementById('modal');
    const slideContainer = document.getElementById('slide');

    // Starts to observe the selected father element with the configured options
    observer.observe(mainContent, observerOptions);
    observer.observe(modalContainer, observerOptions);
    observer.observe(slideContainer, observerOptions);
});


