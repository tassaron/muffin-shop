export function getNodeOrError(name) {
    const node = document.getElementById(name);
    if (!node) {
        throw new ReferenceError(`Missing DOM node with ID ${name}`);
    }
    return node;
}


export function getChildOrError(parentNode, className) {
    const nodes = parentNode.getElementsByClassName(className);
    if (nodes.length != 1) {
        throw new ReferenceError(`${parentNode.className} has ${nodes.length} DOM nodes with class "${className}"; there should be 1`);
    }
    return nodes[0];
}