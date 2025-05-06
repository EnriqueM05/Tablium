// Function to add a character to the expression input
function agregar(caracter) {
  const expresionInput = document.getElementById("expresion");
  expresionInput.value += caracter;
  expresionInput.focus();
}

// Function to clear the expression input
function borrarExpresion() {
  const expresionInput = document.getElementById("expresion");
  expresionInput.value = "";
  document.getElementById("resultado").innerHTML = "";
  expresionInput.focus();
}

// Function to safely evaluate logical expressions
function evaluateLogicalExpression(expression, values) {
  // Create a safer evaluation function that doesn't use eval()
  function parse(expr) {
    // Replace variables with their boolean values
    let parsedExpr = expr;
    for (const variable in values) {
      const regex = new RegExp(`\\b${variable}\\b`, "g");
      parsedExpr = parsedExpr.replace(regex, values[variable].toString());
    }

    // First handle parentheses
    while (parsedExpr.includes("(")) {
      parsedExpr = parsedExpr.replace(/\(([^()]*)\)/g, (match, subExpr) => {
        return parse(subExpr);
      });
    }

    // Handle negation (~)
    parsedExpr = parsedExpr.replace(/~\s*(true|false)/g, (match, value) => {
      return value === "true" ? "false" : "true";
    });

    // Handle conjunction (∧)
    while (parsedExpr.includes("∧")) {
      parsedExpr = parsedExpr.replace(
        /(true|false)\s*∧\s*(true|false)/g,
        (match, left, right) => {
          return left === "true" && right === "true" ? "true" : "false";
        }
      );
    }

    // Handle disjunction (∨)
    while (parsedExpr.includes("∨")) {
      parsedExpr = parsedExpr.replace(
        /(true|false)\s*∨\s*(true|false)/g,
        (match, left, right) => {
          return left === "true" || right === "true" ? "true" : "false";
        }
      );
    }

    // Handle implication (→)
    while (parsedExpr.includes("→")) {
      parsedExpr = parsedExpr.replace(
        /(true|false)\s*→\s*(true|false)/g,
        (match, left, right) => {
          return left === "true" && right === "false" ? "false" : "true";
        }
      );
    }

    // Handle biconditional (↔)
    while (parsedExpr.includes("↔")) {
      parsedExpr = parsedExpr.replace(
        /(true|false)\s*↔\s*(true|false)/g,
        (match, left, right) => {
          return left === right ? "true" : "false";
        }
      );
    }

    // Handle exclusive or (⊕)
    while (parsedExpr.includes("⊕")) {
      parsedExpr = parsedExpr.replace(
        /(true|false)\s*⊕\s*(true|false)/g,
        (match, left, right) => {
          return left !== right ? "true" : "false";
        }
      );
    }

    return parsedExpr;
  }

  // Convert variables to boolean values
  const boolValues = {};
  for (const variable in values) {
    boolValues[variable] = values[variable] ? "true" : "false";
  }

  // Evaluate the expression
  const result = parse(expression);
  return result === "true";
}

// Function to validate the expression
function validarExpresion(expresion) {
  // Basic validation - check for balanced parentheses
  let count = 0;
  for (let i = 0; i < expresion.length; i++) {
    if (expresion[i] === "(") count++;
    if (expresion[i] === ")") count--;
    if (count < 0) return false;
  }
  return count === 0;
}

// Function to generate the truth table
function generarTabla() {
  const expresion = document.getElementById("expresion").value.trim();
  if (!expresion) {
    alert("favor de ingresar una expresión lógica.");
    return;
  }

  if (!validarExpresion(expresion)) {
    alert("la expresión tiene paréntesis desequilibrados.");
    return;
  }

  try {
    // Extract variables from expression
    const variablesSet = new Set();
    for (let i = 0; i < expresion.length; i++) {
      const char = expresion[i];
      if (/[a-z]/.test(char)) {
        variablesSet.add(char);
      }
    }
    const variables = Array.from(variablesSet).sort();

    if (variables.length === 0) {
      alert("No se encontraron variables en la expresión.");
      return;
    }

    const numRows = Math.pow(2, variables.length);
    const truthTable = [];

    // Generate truth table rows
    for (let i = 0; i < numRows; i++) {
      const row = {};
      variables.forEach((variable, index) => {
        row[variable] = Boolean((i >> (variables.length - index - 1)) & 1);
      });
      truthTable.push(row);
    }

    // Evaluate each row
    const resultados = truthTable.map((row) => {
      try {
        return evaluateLogicalExpression(expresion, row);
      } catch (error) {
        console.error("Error evaluating expression:", error);
        return null;
      }
    });

    // Display the truth table
    const resultadoDiv = document.getElementById("resultado");
    let html = '<table border="1"><tr>';
    variables.forEach((variable) => {
      html += `<th>${variable}</th>`;
    });
    html += `<th>${expresion}</th></tr>`;

    truthTable.forEach((row, index) => {
      html += "<tr>";
      variables.forEach((variable) => {
        html += `<td>${row[variable] ? "1" : "0"}</td>`;
      });

      if (resultados[index] === null) {
        html += "<td>Error</td></tr>";
      } else {
        html += `<td>${resultados[index] ? "1" : "0"}</td></tr>`;
      }
    });

    html += "</table>";
    resultadoDiv.innerHTML = html;
  } catch (error) {
    console.error("Error generating truth table:", error);
    alert(
      "Ocurrió un error al generar la tabla de verdad. Verifique la expresión."
    );
  }
}

// Add keyboard event listener for Enter key
document.addEventListener("DOMContentLoaded", function () {
  const inputField = document.getElementById("expresion");
  inputField.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      generarTabla();
    }
  });
});
