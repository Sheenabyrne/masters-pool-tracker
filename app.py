<!DOCTYPE html>
<html>
<head>
    <title>Masters Pool Leaderboard</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #0b3d2e; /* Masters green */
            color: white;
            text-align: center;
            margin: 0;
            padding: 20px;
        }

        h1 {
            color: #f7c948; /* Masters yellow */
            margin-bottom: 20px;
        }

        table {
            margin: auto;
            border-collapse: collapse;
            width: 80%;
            background-color: white;
            color: black;
            border-radius: 10px;
            overflow: hidden;
        }

        th {
            background-color: #0b3d2e;
            color: #f7c948;
            padding: 12px;
            font-size: 18px;
        }

        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }

        tr:nth-child(even) {
            background-color: #f4f4f4;
        }

        tr:hover {
            background-color: #e6f2ef;
        }

        .leader {
            background-color: #f7c948 !important;
            color: black;
            font-weight: bold;
        }

        .footer {
            margin-top: 20px;
            font-size: 12px;
            color: #ccc;
        }
    </style>
</head>

<body>

    <h1>🏆 Masters Pool Leaderboard</h1>

    <table>
        <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Total Score</th>
        </tr>

        {% for person in results %}
        <tr class="{% if loop.index == 1 %}leader{% endif %}">
            <td>{{ loop.index }}</td>
            <td>{{ person.name }}</td>
            <td>{{ person.total }}</td>
        </tr>
        {% endfor %}
    </table>

    <div class="footer">
        Augusta vibes 🌿 | Updated manually
    </div>

</body>
</html>
