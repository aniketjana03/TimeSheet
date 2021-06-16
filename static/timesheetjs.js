$(document).ready(function(){

      const weekDays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];

      $('#datePicker').datepicker({ //initiate JQueryUI datepicker
        showAnim: 'fadeIn',
        dateFormat: "dd/mm/yy",
        firstDay: 6, //first day is Monday
        beforeShowDay: function(date) {
          //only allow Mondays to be selected
          return [date.getDay() == 6,""];
        },
        onSelect: populateDates
      });

      function populateDates() {

        $('#tBody').empty(); //clear table
        $('.bottom').removeClass('d-none'); //display total hours worked
        let chosenDate = $('#datePicker').datepicker('getDate'); //get chosen date from datepicker
        let newDate;
        const monStartWeekDays = ['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday'];
        for(let i = 0; i < weekDays.length; i++) { //iterate through each weekday
          newDate = new Date(chosenDate); //create date object
          newDate.setDate(chosenDate.getDate() + i); //increment set date
          //append results to table
          $('#tBody').append( `
          <tr>
            <td class="day">${weekDays[newDate.getDay()].slice(0,3)}</td>
            <td class="date">${newDate.getDate()} / ${newDate.getMonth() + 1} / ${newDate.getFullYear()}</td>
            <td><input type="hidden" name="td${i + 1}" value="${newDate.getDate()}/${newDate.getMonth() + 1}/${newDate.getFullYear()}"></td>
            <td class="break">
              <select id="break${monStartWeekDays[i]}">
                <option value="1">Present</option>
                <option value="0">Leave</option>
                <option value="2">Half-Day</option>
              </select>
            </td>
            <td><input type="hidden" id="stat${monStartWeekDays[i]}" name="status${monStartWeekDays[i]}" value="1"></td>
          </tr>
          ` );
          //function to calculate hours worked
          let calculateHours = () => {
            let startVal = $(`#startTime${monStartWeekDays[i]}`).val();
            let finishVal = $(`#finishTime${monStartWeekDays[i]}`).val();
            let startTime = new Date( `01/01/2007 ${startVal}` );
            let finishTime = new Date( `01/01/2007 ${finishVal}` );
            let breakTime = $(`#break${monStartWeekDays[i]}`).val();
            let hoursWorked = (finishTime.getTime() - startTime.getTime()) / 1000;
            let status = $(`#break${monStartWeekDays[i]}`).val();
            hoursWorked /= (60 * 60);
            $(`#stat${monStartWeekDays[i]}`).val(status);

            if (startVal && finishVal && breakTime=="1") { //providing both start and finish times are set
              if (hoursWorked >= 0) { //if normal day shift
                $(`#hoursWorked${monStartWeekDays[i]}`).html(hoursWorked);
              } else { //if night shift
                $(`#hoursWorked${monStartWeekDays[i]}`).html(24 + hoursWorked);
              }
            }
            else if (breakTime!="1")
            {
              hoursWorked = 0;
              $(`#hoursWorked${monStartWeekDays[i]}`).html(hoursWorked);
            }

          }
          //initiate function whenever an input value is changed
          $(`#startTime${monStartWeekDays[i]}, #finishTime${monStartWeekDays[i]}, #break${monStartWeekDays[i]}`).on('change', calculateHours);

        }
        $('.start-time input').timepicker({ 'timeFormat': 'H:i', 'step': 15, 'scrollDefault': '09:00' });
        $('.finish-time input').timepicker({ 'timeFormat': 'H:i', 'step': 15, 'scrollDefault': '17:00' });




      }


    });
