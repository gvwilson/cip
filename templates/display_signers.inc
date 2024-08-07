{% if signers %}
  <table class="signers">
    <thead>
      <tr>
        <th>Name</th>
        <th>Affiliation</th>
        <th>Country</th>
        <th>Date</th>
      </tr>
    </thead>
    <tbody>
      {% for s in signers %}
      <tr>
        <td>{{s.fullname}}</td>
        <td>{{s.affiliation}}</td>
        <td>{{s.country}}</td>
        <td>{{s.created}}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
{% else %}
  <p>no signers</p>
{% endif %}
