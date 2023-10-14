import React, { useEffect } from 'react';

function TimelineComponent({ timelineData }) {
  useEffect(() => {
    // Parse the timeline data
    console.log(timelineData)
    const parsedTimelineData = timelineData;
 
    // Create an array to store the timeline events
    const timelineEvents = [];

    // Iterate over the timeline data and create events
    for (let i = 0; i < parsedTimelineData.length; i++) {
      const event = {
        start_date: new Date(parsedTimelineData[i].date),
        text: {
          headline: "Version "+  parseInt(parsedTimelineData[i].version +1),
          text: `<strong>New rows:</strong> ${parsedTimelineData[i].rows}<br><strong>New columns:</strong> ${parsedTimelineData[i].columns}<br><strong>Start date:</strong> ${parsedTimelineData[i].first_index}<br><strong>End date:</strong> ${parsedTimelineData[i].last_index}`,
        },
      };
      timelineEvents.push(event);
    }

    // Create the timeline JSON object
    const timelineJson = {
      events: timelineEvents,
    };

    // Initialize the timeline
    window.timeline = new TL.Timeline('timeline', timelineJson);
  }, [timelineData]);

  return (
  <>

  
  <div id="timeline"></div>
  
</>)
}
export default TimelineComponent
